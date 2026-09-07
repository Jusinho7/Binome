/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log_utils.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:39:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/07 19:39:01 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	log_event(t_sim *sim, int coder_id, const char *msg)
{
	long long	ts;

	ts = get_time_ms(sim);
	pthread_mutex_lock(&sim->print_lock);
	printf("%lld %d %s\n", ts, coder_id, msg);
	fflush(stdout);
	pthread_mutex_unlock(&sim->print_lock);
}
