/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 18:45:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/08 18:45:13 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# ifndef _DEFAULT_SOURCE
#  define _DEFAULT_SOURCE
# endif

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <time.h>

typedef struct s_sim	t_sim;

/*
** Une demande de dongle dans la file d'attente d'un dongle.
** key = priorite : plus la valeur est PETITE, plus le coder passe tot.
**   - fifo : key = numero d'arrivee (ticket)
**   - edf  : key = deadline (last_compile_start + time_to_burnout)
** En cas d'egalite, le plus petit coder_id gagne (regle deterministe).
*/
typedef struct s_req
{
	int		coder_id;
	long	key;
}	t_req;

/* Tas binaire (min-heap) : data[0] est toujours la demande prioritaire. */
typedef struct s_heap
{
	t_req	*data;
	int		size;
	int		cap;
}	t_heap;

/*
** Un dongle. Tout son etat est protege par SON mutex :
**   in_use       : 1 si un coder le tient en main
**   available_at : date (ms) a partir de laquelle il est reutilisable
**                  (fin du cooldown)
**   version      : compteur +1 a chaque fois que le dongle est rendu
**                  (sert a savoir qu'il s'est passe quelque chose)
**   queue        : file d'attente des coders qui le demandent
*/
typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	int				in_use;
	long			available_at;
	long			version;
	t_heap			queue;
}	t_dongle;

/*
** Un coder (= un thread).
**   lock : protege last_compile_start et compile_count, car le
**          monitor les lit pendant que le coder les modifie.
**   first / second : les 2 dongles, TOUJOURS pris dans le meme ordre
**          global (le plus petit indice d'abord) => pas de deadlock.
*/
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

/* Toute la simulation : parametres + ressources partagees. */
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

/* parse.c */
int		parse_args(int argc, char **argv, t_sim *sim);

/* init.c / cleanup.c / run.c */
int		init_sim(t_sim *sim);
void	destroy_sim(t_sim *sim);
int		run_simulation(t_sim *sim);

/* coder.c / monitor.c */
void	*coder_routine(void *arg);
void	*monitor_routine(void *arg);

/* dongle.c */
int		dongle_acquire(t_dongle *d, t_coder *c);
void	dongle_release(t_dongle *d, t_sim *sim);
void	dongle_give_back(t_dongle *d);
int		acquire_pair(t_coder *c);

/* heap.c / heap_utils.c */
int		heap_init(t_heap *h, int cap);
void	heap_free(t_heap *h);
int		heap_push(t_heap *h, t_req req);
t_req	heap_pop(t_heap *h);
int		heap_peek_id(t_heap *h);
int		req_less(t_req *a, t_req *b);
void	sift_up(t_heap *h, int i);
void	sift_down(t_heap *h, int i);

/* state.c */
int		is_stopped(t_sim *sim);
void	set_stop(t_sim *sim);
void	wake_all(t_sim *sim);
void	log_event(t_coder *c, const char *msg);
void	log_burnout(t_sim *sim, int id);

/* time_utils.c */
long	now_ms(void);
void	smart_sleep(t_sim *sim, long duration);
void	make_abs_timeout(struct timespec *ts, long remaining_ms);

#endif
