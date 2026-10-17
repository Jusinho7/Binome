/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/17 22:51:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/17 22:55:01 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	set_single_coder(t_sim *sim, int i)
{
	sim->coders[i].id = i + 1;
	sim->coders[i].sim = sim;
	sim->coders[i].compile_count = 0;
	sim->coders[i].request_key = 0;
	sim->coders[i].last_compile_start = 0;
	sim->coders[i].first = &sim->dongles[0];
	sim->coders[i].second = NULL;
}

void	set_pair_coder(t_sim *sim, int i)
{
	t_coder	*c;
	int		left;
	int		right;

	c = &sim->coders[i];
	left = i;
	right = (i + 1) % sim->n;
	c->id = i + 1;
	c->sim = sim;
	c->compile_count = 0;
	c->request_key = 0;
	c->last_compile_start = 0;
	if (left < right)
	{
		c->first = &sim->dongles[left];
		c->second = &sim->dongles[right];
	}
	else
	{
		c->first = &sim->dongles[right];
		c->second = &sim->dongles[left];
	}
}
