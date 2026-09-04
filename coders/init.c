#include "codexion.h"

static void	init_coder(t_sim *sim, int i)
{
	sim->coders[i].id = i + 1;
	sim->coders[i].sim = sim;
	sim->coders[i].compiles_done = 0;
	sim->coders[i].burned_out = 0;
	sim->coders[i].state = STATE_IDLE;
	sim->coders[i].last_compile_start = 0;
	pthread_mutex_init(&sim->coders[i].state_lock, NULL);
	sim->coders[i].right = &sim->dongles[i];
	sim->coders[i].left = &sim->dongles[(i - 1 + sim->n_coders) % sim->n_coders];
}

int	init_sim(t_sim *sim)
{
	int	i;

	sim->coders = malloc(sizeof(t_coder) * sim->n_coders);
	sim->dongles = malloc(sizeof(t_dongle) * sim->n_coders);
	if (!sim->coders || !sim->dongles)
		return (0);
	i = 0;
	while (i < sim->n_coders)
	{
		dongle_init(&sim->dongles[i], i);
		i++;
	}
	i = 0;
	while (i < sim->n_coders)
	{
		init_coder(sim, i);
		i++;
	}
	pthread_mutex_init(&sim->print_lock, NULL);
	pthread_mutex_init(&sim->stop_lock, NULL);
	sim->stop = 0;
	return (1);
}
