/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:38:42 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/07 21:24:45 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	do_phase(t_coder *c, int state, long long duration, const char *msg)
{
	t_sim	*sim;

	pthread_mutex_lock(&c->state_lock);
	c->state = state;
	pthread_mutex_unlock(&c->state_lock);
	sim = c->sim;
	log_event(sim, c->id, msg);
	sleep_ms(duration);
}

static int	take_dongles(t_coder *c, t_dongle *first, t_dongle *second)
{
	if (!dongle_acquire(first, c, c->sim))
		return (0);
	log_event(c->sim, c->id, "has taken a dongle");
	if (first == second)
		return (1);
	if (!dongle_acquire(second, c, c->sim))
	{
		dongle_release(first, c->sim);
		return (0);
	}
	log_event(c->sim, c->id, "has taken a dongle");
	return (1);
}

static void	do_compile(t_coder *c, t_dongle *a, t_dongle *b)
{
	pthread_mutex_lock(&c->state_lock);
	c->last_compile_start = get_time_ms(c->sim);
	c->state = STATE_COMPILING;
	pthread_mutex_unlock(&c->state_lock);
	log_event(c->sim, c->id, "is compiling");
	sleep_ms(c->sim->time_to_compile);
	if (a == b)
		dongle_release(a, c->sim);
	else
	{
		dongle_release(a, c->sim);
		dongle_release(b, c->sim);
	}
	pthread_mutex_lock(&c->state_lock);
	c->compiles_done++;
	pthread_mutex_unlock(&c->state_lock);
}

static int	coder_step(t_coder *c, t_dongle *first, t_dongle *second)
{
	if (!take_dongles(c, first, second))
		return (0);
	if (sim_is_stopped(c->sim))
	{
		dongle_release(first, c->sim);
		if (first != second)
			dongle_release(second, c->sim);
		return (0);
	}
	do_compile(c, first, second);
	if (sim_is_stopped(c->sim))
		return (0);
	do_phase(c, STATE_DEBUGGING, c->sim->time_to_debug,
		"is debugging");
	if (sim_is_stopped(c->sim))
		return (0);
	do_phase(c, STATE_REFACTORING, c->sim->time_to_refactor,
		"is refactoring");
	return (1);
}

void	*coder_routine(void *arg)
{
	t_coder		*c;
	t_dongle	*first;
	t_dongle	*second;

	c = arg;
	c->last_compile_start = get_time_ms(c->sim);
	first = c->left;
	second = c->right;
	if (first->id > second->id)
	{
		first = c->right;
		second = c->left;
	}
	while (!sim_is_stopped(c->sim) && coder_step(c, first, second))
		;
	return (NULL);
}
