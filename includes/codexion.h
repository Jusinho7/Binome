/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 18:45:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/13 17:33:38 by srasolov         ###   ########.fr       */
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

typedef struct s_sim	t_sim;

typedef struct s_req
{
	int		coder_id;
	long	key;
}	t_req;

typedef struct s_heap
{
	t_req	*data;
	int		size;
	int		cap;
}	t_heap;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	int				in_use;
	long			available_at;
	long			version;
	t_heap			queue;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	pthread_mutex_t	lock;
	long			last_compile_start;
	int				compile_count;
	long			request_key;
	t_dongle		*first;
	t_dongle		*second;
	t_sim			*sim;
}	t_coder;

struct s_sim
{
	int				n;
	long			t_burnout;
	long			t_compile;
	long			t_debug;
	long			t_refactor;
	int				compiles_required;
	long			cooldown;
	int				use_edf;
	long			start;
	int				stop;
	pthread_mutex_t	stop_mutex;
	pthread_mutex_t	log_mutex;
	t_dongle		*dongles;
	t_coder			*coders;
	pthread_t		monitor;
	int				dongles_ready;
	int				coders_ready;
	int				locks_ready;
	int				coders_started;
};

int		parse_args(int argc, char **argv, t_sim *sim);

int		init_sim(t_sim *sim);
void	destroy_sim(t_sim *sim);
int		run_simulation(t_sim *sim);

void	*coder_routine(void *arg);
void	*monitor_routine(void *arg);

int		dongle_acquire(t_dongle *d, t_coder *c);
void	dongle_release(t_dongle *d, t_sim *sim);
void	dongle_give_back(t_dongle *d);
int		acquire_pair(t_coder *c);

int		heap_init(t_heap *h, int cap);
void	heap_free(t_heap *h);
int		heap_push(t_heap *h, t_req req);
t_req	heap_pop(t_heap *h);
int		heap_peek_id(t_heap *h);
int		req_less(t_req *a, t_req *b);
void	sift_up(t_heap *h, int i);
void	sift_down(t_heap *h, int i);

int		is_stopped(t_sim *sim);
void	set_stop(t_sim *sim);
void	wake_all(t_sim *sim);
void	log_event(t_coder *c, const char *msg);
void	log_burnout(t_sim *sim, int id);

long	now_ms(void);
void	smart_sleep(t_sim *sim, long duration);
void	make_abs_timeout(struct timespec *ts, long remaining_ms);

#endif
