#include "codexion.h"

void	dongle_init(t_dongle *d, int id)
{
	d->id = id;
	pthread_mutex_init(&d->lock, NULL);
	pthread_cond_init(&d->cond, NULL);
	d->in_use = 0;
	d->never_used = 1;
	d->free_since = 0;
	d->waiters = NULL;
}

void	dongle_destroy(t_dongle *d)
{
	pthread_mutex_destroy(&d->lock);
	pthread_cond_destroy(&d->cond);
}

static void	waiter_add(t_waiter **list, t_waiter *w)
{
	w->next = *list;
	*list = w;
}

static void	waiter_remove(t_waiter **list, t_waiter *w)
{
	t_waiter	**cur;

	cur = list;
	while (*cur)
	{
		if (*cur == w)
		{
			*cur = w->next;
			return ;
		}
		cur = &(*cur)->next;
	}
}

static t_waiter	*select_waiter(t_waiter *list, int scheduler)
{
	t_waiter	*best;
	t_waiter	*cur;

	if (!list)
		return (NULL);
	best = list;
	cur = list->next;
	while (cur)
	{
		if (scheduler == SCHED_EDF_MODE)
		{
			if (cur->deadline < best->deadline
				|| (cur->deadline == best->deadline && cur->arrival < best->arrival))
				best = cur;
		}
		else if (cur->arrival < best->arrival)
			best = cur;
		cur = cur->next;
	}
	return (best);
}

static int	dongle_ready(t_dongle *d, t_waiter *w, t_sim *sim, long long now)
{
	int	cooldown_ok;

	cooldown_ok = d->never_used || (now - d->free_since >= sim->dongle_cooldown);
	return (!d->in_use && cooldown_ok && select_waiter(d->waiters, sim->scheduler) == w);
}

int	dongle_acquire(t_dongle *d, t_coder *c, t_sim *sim)
{
	t_waiter		w;
	struct timespec	ts;
	long long		wait_until;

	w.coder_id = c->id;
	w.arrival = get_time_ms(sim);
	w.deadline = c->last_compile_start + sim->time_to_burnout;
	pthread_mutex_lock(&d->lock);
	waiter_add(&d->waiters, &w);
	while (!sim_is_stopped(sim))
	{
		if (dongle_ready(d, &w, sim, get_time_ms(sim)))
		{
			d->in_use = 1;
			d->never_used = 0;
			waiter_remove(&d->waiters, &w);
			pthread_mutex_unlock(&d->lock);
			return (1);
		}
		if (!d->in_use && !d->never_used)
			wait_until = d->free_since + sim->dongle_cooldown;
		else
			wait_until = get_time_ms(sim) + 5;
		ms_to_abs_timespec(sim, wait_until, &ts);
		pthread_cond_timedwait(&d->cond, &d->lock, &ts);
	}
	waiter_remove(&d->waiters, &w);
	pthread_mutex_unlock(&d->lock);
	return (0);
}

void	dongle_release(t_dongle *d, t_sim *sim)
{
	pthread_mutex_lock(&d->lock);
	d->in_use = 0;
	d->free_since = get_time_ms(sim);
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->lock);
}
