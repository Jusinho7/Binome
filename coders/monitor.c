#include "codexion.h"

void	sim_stop(t_sim *sim)
{
	pthread_mutex_lock(&sim->stop_lock);
	sim->stop = 1;
	pthread_mutex_unlock(&sim->stop_lock);
}

int	sim_is_stopped(t_sim *sim)
{
	int	v;

	pthread_mutex_lock(&sim->stop_lock);
	v = sim->stop;
	pthread_mutex_unlock(&sim->stop_lock);
	return (v);
}

static int	check_burnout(t_sim *sim, int i)
{
	long long	now;
	int			burned;

	pthread_mutex_lock(&sim->coders[i].state_lock);
	now = get_time_ms(sim);
	burned = 0;
	if (sim->coders[i].state != STATE_COMPILING
		&& !sim->coders[i].burned_out
		&& now - sim->coders[i].last_compile_start > sim->time_to_burnout)
	{
		sim->coders[i].burned_out = 1;
		sim->coders[i].state = STATE_BURNED;
		burned = 1;
	}
	pthread_mutex_unlock(&sim->coders[i].state_lock);
	return (burned);
}

static int	check_all_done(t_sim *sim, int i)
{
	int	done;

	pthread_mutex_lock(&sim->coders[i].state_lock);
	done = (sim->coders[i].compiles_done >= sim->n_compiles_required);
	pthread_mutex_unlock(&sim->coders[i].state_lock);
	return (done);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	int		i;
	int		all_done;

	sim = arg;
	while (!sim_is_stopped(sim))
	{
		usleep(1000);
		all_done = 1;
		i = 0;
		while (i < sim->n_coders)
		{
			if (check_burnout(sim, i))
			{
				log_event(sim, sim->coders[i].id, "burned out");
				sim_stop(sim);
				return (NULL);
			}
			if (!check_all_done(sim, i))
				all_done = 0;
			i++;
		}
		if (all_done)
		{
			sim_stop(sim);
			return (NULL);
		}
	}
	return (NULL);
}
