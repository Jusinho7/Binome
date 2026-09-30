/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/01 00:52:22 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/01 01:16:53 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	wait_single_dongle(t_sim *sim, t_dongle *d)
{
	pthread_mutex_lock(&d->lock);
	while (!sim_is_stopped(sim))
		pthread_cond_wait(&d->cond, &d->lock);
	pthread_mutex_unlock(&d->lock);
}

static void	order_dongles(t_coder *coder, t_dongle **first, t_dongle **second)
{
	if (coder->left->id < coder->right->id)
	{
		*first = coder->left;
		*second = coder->right;
	}
	else
	{
		*first = coder->right;
		*second = coder->left;
	}
}

static void	release_one(t_sim *sim, t_dongle *d)
{
	pthread_mutex_lock(&d->lock);
	d->in_use = 0;
	d->free_since = get_now_ms(sim);
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->lock);
}

int	acquire_dongles(t_coder *coder)
{
	t_sim		*sim;
	t_dongle	*first;
	t_dongle	*second;

	sim = coder->sim;
	if (coder->left == coder->right)
	{
		wait_single_dongle(sim, coder->left);
		return (0);
	}
	order_dongles(coder, &first, &second);
	if (!acquire_one(sim, coder, first))
		return (0);
	log_state(sim, coder->id, "has taken a dongle");
	if (!acquire_one(sim, coder, second))
	{
		release_one(sim, first);
		return (0);
	}
	log_state(sim, coder->id, "has taken a dongle");
	return (1);
}

void	release_dongles(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (coder->left == coder->right)
		return ;
	release_one(sim, coder->left);
	release_one(sim, coder->right);
}
