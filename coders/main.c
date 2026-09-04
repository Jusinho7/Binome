#include "codexion.h"

static int	start_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		if (pthread_create(&sim->coders[i].thread, NULL,
				coder_routine, &sim->coders[i]) != 0)
		{
			fprintf(stderr, "Error: thread creation failed\n");
			sim_stop(sim);
			return (0);
		}
		i++;
	}
	return (1);
}

static void	join_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		pthread_join(sim->coders[i].thread, NULL);
		i++;
	}
}

int	main(int argc, char **argv)
{
	t_sim	sim;

	if (!parse_args(argc, argv, &sim))
	{
		fprintf(stderr, "Error: invalid arguments\n");
		return (1);
	}
	if (!init_sim(&sim))
	{
		fprintf(stderr, "Error: initialization failed\n");
		return (1);
	}
	gettimeofday(&sim.start_time, NULL);
	if (!start_coders(&sim))
	{
		join_coders(&sim);
		free_sim(&sim);
		return (1);
	}
	pthread_create(&sim.monitor, NULL, monitor_routine, &sim);
	join_coders(&sim);
	pthread_join(sim.monitor, NULL);
	free_sim(&sim);
	return (0);
}
