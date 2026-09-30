/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/06 05:23:13 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/30 10:34:05 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <sys/time.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>

# define SCHED_FIFO_MODE 0
# define SCHED_EDF_MODE 1

# define STATE_IDLE 0
# define STATE_WAITING 1
# define STATE_COMPILING 2
# define STATE_DEBUGGING 3
# define STATE_REFACTORING 4
# define STATE_BURNED 5

typedef struct s_waiter
{
	int					coder_id;
	long long			arrival;
	long long			deadline;
}	t_waiter;

typedef struct s_heap
{
	t_waiter			data[2];
	int					size;
	int					mode;
}	t_heap;

typedef struct s_dongle
{
	int					id;
	pthread_mutex_t		lock;
	pthread_cond_t		cond;
	int					in_use;
	int					never_used;
	long long			free_since;
	t_heap				waiters;
}	t_dongle;

typedef struct s_sim	t_sim;

typedef struct s_coder
{
	int					id;
	pthread_t			thread;
	t_dongle			*left;
	t_dongle			*right;
	long long			last_compile_start;
	int					compiles_done;
	int					state;
	int					burned_out;
	pthread_mutex_t		state_lock;
	t_sim				*sim;
}	t_coder;

struct s_sim
{
	int					n_coders;
	long long			time_to_burnout;
	long long			time_to_compile;
	long long			time_to_debug;
	long long			time_to_refactor;
	int					n_compiles_required;
	long long			dongle_cooldown;
	int					scheduler;
	struct timeval		start_time;
	t_dongle			*dongles;
	t_coder				*coders;
	pthread_mutex_t		print_lock;
	pthread_mutex_t		stop_lock;
	int					stop;
	pthread_t			monitor;
};

int			parse_args(int argc, char **argv, t_sim *sim);
int			init_sim(t_sim *sim);
void		free_sim(t_sim *sim);

void		heap_push(t_heap *h, t_waiter w);
void		heap_pop(t_heap *h);
t_waiter	heap_peek(t_heap *h);
int			heap_remove(t_heap *h, int coder_id);
int			heap_is_better(t_heap *h, t_waiter *a, t_waiter *b);
void		heap_swap(t_waiter *a, t_waiter *b);
void		heap_sift_up(t_heap *h, int i);
void		heap_sift_down(t_heap *h, int i);

#endif