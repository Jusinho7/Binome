/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:23:05 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/14 06:32:54 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	take_dongles(t_coder *c)
{
	if (!acquire_pair(c))
		return (0);
	log_event(c, "\033[38;5;46mhas taken a dongle\033[0m");
	log_event(c, "\033[38;5;46mhas taken a dongle\033[0m");
	return (1);
}

static void	do_compile(t_coder *c)
{
	pthread_mutex_lock(&c->lock);
	c->last_compile_start = now_ms();
	pthread_mutex_unlock(&c->lock);
	log_event(c, "\033[38;5;39mis compiling\033[0m");
	smart_sleep(c->sim, c->sim->t_compile);
	pthread_mutex_lock(&c->lock);
	c->compile_count++;
	pthread_mutex_unlock(&c->lock);
	dongle_release(c->first, c->sim);
	dongle_release(c->second, c->sim);
}

static void	lonely_coder(t_coder *c)
{
	if (!dongle_acquire(c->first, c))
		return ;
	log_event(c, "\033[38;5;46mhas taken a dongle\033[0m");
	while (!is_stopped(c->sim))
		usleep(500);
	dongle_release(c->first, c->sim);
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
		log_event(c, "\033[38;5;51mis debugging\033[0m");
		smart_sleep(c->sim, c->sim->t_debug);
		log_event(c, "\033[38;5;201mis refactoring\033[0m");
		smart_sleep(c->sim, c->sim->t_refactor);
	}
	return (NULL);
}
