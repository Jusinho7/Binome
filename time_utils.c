/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/01 01:15:41 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/01 01:26:44 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long long	get_now_ms(t_sim *sim)
{
	struct timeval	now;
	long long		start_us;
	long long		now_us;

	gettimeofday(&now, NULL);
	start_us = (long long)sim->start_time.tv_sec * 1000000LL
		+ sim->start_time.tv_usec;
	now_us = (long long)now.tv_sec * 1000000LL + now.tv_usec;
	return ((now_us - start_us) / 1000LL);
}

void	ms_to_timespec(t_sim *sim, long long target_ms, struct timespec *ts)
{
	long long	target_us;

	target_us = (long long)sim->start_time.tv_usec + target_ms * 1000LL;
	ts->tv_sec = sim->start_time.tv_sec + target_us / 1000000LL;
	ts->tv_nsec = (target_us % 1000000LL) * 1000LL;
}