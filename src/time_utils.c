/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:41:34 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:41:47 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	now_ms(void)
{
	struct timespec	ts;

	clock_gettime(CLOCK_MONOTONIC, &ts);
	return (ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
}

void	smart_sleep(t_sim *sim, long duration)
{
	long	end;

	end = now_ms() + duration;
	while (now_ms() < end && !is_stopped(sim))
		usleep(500);
}

void	make_abs_timeout(struct timespec *ts, long remaining_ms)
{
	clock_gettime(CLOCK_REALTIME, ts);
	ts->tv_sec += remaining_ms / 1000;
	ts->tv_nsec += (remaining_ms % 1000) * 1000000;
	if (ts->tv_nsec >= 1000000000)
	{
		ts->tv_sec += 1;
		ts->tv_nsec -= 1000000000;
	}
}
