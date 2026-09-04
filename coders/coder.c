#include "codexion.h"

static void	set_state(t_coder *c, int state)
{
	pthread_mutex_lock(&c->state_lock);
	c->state = state;
	pthread_mutex_unlock(&c->state_lock);
}

static void	do_phase(t_sim *sim, t_coder *c, int state,
		long long duration, const char *msg)
{
	set_state(c, state);
	log_event(sim, c->id, msg);
	sleep_ms(duration);
}

static int	acquire_both(t_sim *sim, t_coder *c, t_dongle *a, t_dongle *b)
{
	if (a == b)
	{
		if (!dongle_acquire(a, c, sim))
			return (0);
		log_event(sim, c->id, "has taken a dongle");
		log_event(sim, c->id, "has taken a dongle");
		return (1);
	}
	if (!dongle_acquire(a, c, sim))
		return (0);
	log_event(sim, c->id, "has taken a dongle");
	if (!dongle_acquire(b, c, sim))
	{
		dongle_release(a, sim);
		return (0);
	}
	log_event(sim, c->id, "has taken a dongle");
	return (1);
}

static void	release_both(t_sim *sim, t_dongle *a, t_dongle *b)
{
	if (a == b)
	{
		dongle_release(a, sim);
		return ;
	}
	dongle_release(a, sim);
	dongle_release(b, sim);
}

static void	do_compile(t_sim *sim, t_coder *c, t_dongle *a, t_dongle *b)
{
	pthread_mutex_lock(&c->state_lock);
	c->last_compile_start = get_time_ms(sim);
	c->state = STATE_COMPILING;
	pthread_mutex_unlock(&c->state_lock);
	log_event(sim, c->id, "is compiling");
	sleep_ms(sim->time_to_compile);
	release_both(sim, a, b);
	pthread_mutex_lock(&c->state_lock);
	c->compiles_done++;
	pthread_mutex_unlock(&c->state_lock);
}

void	*coder_routine(void *arg)
{
	t_coder		*c;
	t_sim		*sim;
	t_dongle	*first;
	t_dongle	*second;

	c = arg;
	sim = c->sim;
	pthread_mutex_lock(&c->state_lock);
	c->last_compile_start = get_time_ms(sim);
	pthread_mutex_unlock(&c->state_lock);
	if (c->left->id < c->right->id)
	{
		first = c->left;
		second = c->right;
	}
	else
	{
		first = c->right;
		second = c->left;
	}
	while (!sim_is_stopped(sim))
	{
		if (!acquire_both(sim, c, first, second))
			break ;
		if (sim_is_stopped(sim))
		{
			release_both(sim, first, second);
			break ;
		}
		do_compile(sim, c, first, second);
		if (sim_is_stopped(sim))
			break ;
		do_phase(sim, c, STATE_DEBUGGING, sim->time_to_debug, "is debugging");
		if (sim_is_stopped(sim))
			break ;
		do_phase(sim, c, STATE_REFACTORING, sim->time_to_refactor, "is refactoring");
	}
	return (NULL);
}
