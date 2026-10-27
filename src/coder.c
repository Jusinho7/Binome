/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:23:05 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 14:29:16 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	take_dongles(t_coder *c)
{
	if (!acquire_pair(c))
		return (0);
	return (1);
}

static void	do_compile(t_coder *c)
{
	pthread_mutex_lock(&c->lock);
	c->last_compile_start = now_ms();
	pthread_mutex_unlock(&c->lock);
	log_event(c, "is compiling");
	smart_sleep(c->sim, c->sim->t_compile);
	pthread_mutex_lock(&c->lock);
	c->compile_count++;
	pthread_mutex_unlock(&c->lock);
	dongle_release(c->first, c->sim);
	if (c->second)
		dongle_release(c->second, c->sim);
}

static void	lonely_coder(t_coder *c)
{
	log_event(c, "has taken a dongle");
	while (!is_stopped(c->sim))
		usleep(500);
}

void	*coder_routine(void *arg)
{
	t_coder	*c;

	c = (t_coder *)arg;
	if (c->sim->n == 1)
	{
		lonely_coder(c);
		return (NULL);
	}
	while (!is_stopped(c->sim))
	{
		if (!take_dongles(c))
			break ;
		do_compile(c);
		if (c->compile_count >= c->sim->compiles_required)
			return (NULL);
		log_event(c, "is debugging");
		smart_sleep(c->sim, c->sim->t_debug);
		log_event(c, "is refactoring");
		smart_sleep(c->sim, c->sim->t_refactor);
	}
	return (NULL);
}
