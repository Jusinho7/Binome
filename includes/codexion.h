/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 18:45:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 19:09:08 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <time.h>

# define RED   "\033[31m"
# define MAGENTA "\033[38;5;201m"
# define GREEN "\033[38;5;46m"
# define BLUE  "\033[38;5;39m"
# define CYAN  "\033[38;5;51m"
# define ORANGE "\033[38;5;208m"
# define RESET "\033[0m"

typedef struct s_sim	t_sim;

typedef struct s_req
{
	int					coder_id;
	long				key;
	unsigned long long	order;
}	t_req;

typedef struct s_queue
{
	t_req				*requests;
	int					size;
	int					capacity;
	int					use_edf;
}	t_queue;

typedef struct s_dongle
{
	int				in_use;
	long			available_at;
	t_queue			queue;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	pthread_mutex_t	lock;
	long			last_compile_start;
	int				compile_count;
	long			request_key;
	t_req			pending;
	t_dongle		*first;
	t_dongle		*second;
	t_sim			*sim;
}	t_coder;

struct s_sim
{
	int					n;
	long				t_burnout;
	long				t_compile;
	long				t_debug;
	long				t_refactor;
	int					compiles_required;
	long				cooldown;
	int					use_edf;
	long				start;
	int					stop;
	pthread_mutex_t		stop_mutex;
	pthread_mutex_t		log_mutex;
	pthread_mutex_t		table_mutex;
	pthread_cond_t		table_cond;
	unsigned long long	next_order;
	t_dongle			*dongles;
	t_coder				*coders;
	pthread_t			monitor;
	int					dongles_ready;
	int					coders_ready;
	int					locks_ready;
	int					coders_started;
};

int		parse_args(int argc, char **argv, t_sim *sim);

int		init_sim(t_sim *sim);
void	destroy_sim(t_sim *sim);
int		run_simulation(t_sim *sim);
void	set_single_coder(t_sim *sim, int i);
void	set_pair_coder(t_sim *sim, int i);

void	*coder_routine(void *arg);
void	*monitor_routine(void *arg);

void	dongle_release(t_dongle *d, t_sim *sim);
int		pair_free(t_coder *c, long t);
int		pair_outranked(t_coder *c, t_dongle *d, long t);
int		acquire_pair(t_coder *c);

int		queue_init(t_queue *q, int capacity);
void	queue_destroy(t_queue *q);
int		queue_add(t_queue *q, t_req req);
int		queue_remove(t_queue *q, int coder_id);
int		queue_peek_id(t_queue *q);
void	queue_heap_add(t_queue *q, t_req req);
void	queue_heap_remove_at(t_queue *q, int index);
int		queue_req_less(t_queue *q, t_req *a, t_req *b);
void	queue_capacity_error(t_sim *sim);
void	queue_set_fifo_policy(t_queue *q);
void	queue_set_edf_policy(t_queue *q);
int		fifo_queue_peek_id(t_queue *q);
int		fifo_req_less(t_req *a, t_req *b);
int		edf_queue_peek_id(t_queue *q);
int		edf_req_less(t_req *a, t_req *b);
long	edf_request_key(t_coder *c);

int		is_stopped(t_sim *sim);
void	set_stop(t_sim *sim);
void	wake_all(t_sim *sim);
void	log_event(t_coder *c, const char *msg);
void	log_burnout(t_sim *sim, int id);

long	now_ms(void);
void	smart_sleep(t_sim *sim, long duration);
void	make_abs_timeout(struct timespec *ts, long remaining_ms);

#endif
