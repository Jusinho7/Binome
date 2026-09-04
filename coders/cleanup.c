#include "codexion.h"

void	free_sim(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		pthread_mutex_destroy(&sim->coders[i].state_lock);
		i++;
	}
	i = 0;
	while (i < sim->n_coders)
	{
		dongle_destroy(&sim->dongles[i]);
		i++;
	}
	pthread_mutex_destroy(&sim->print_lock);
	pthread_mutex_destroy(&sim->stop_lock);
	free(sim->coders);
	free(sim->dongles);
}
