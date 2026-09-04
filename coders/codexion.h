/* ************************************************************************** */
/*                                                                            */
/*                                                        CODEXION            */
/*   codexion.h                                                              */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <sys/time.h>
# include <time.h>
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
	struct s_waiter		*next;
}	t_waiter;

typedef struct s_dongle
{
	int					id;
	pthread_mutex_t		lock;
	pthread_cond_t		cond;
	int					in_use;
	int					never_used;
	long long			free_since;
	t_waiter			*waiters;
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
	t_coder				*coders;
	t_dongle			*dongles;
	pthread_mutex_t		print_lock;
	pthread_mutex_t		stop_lock;
	int					stop;
	pthread_t			monitor;
};

/* parsing.c */
int			parse_args(int argc, char **argv, t_sim *sim);

/* init.c */
int			init_sim(t_sim *sim);

/* time_utils.c */
long long	get_time_ms(t_sim *sim);
void		sleep_ms(long long ms);
void		ms_to_abs_timespec(t_sim *sim, long long ms, struct timespec *ts);

/* log_utils.c */
void		log_event(t_sim *sim, int coder_id, const char *msg);

/* dongle.c */
void		dongle_init(t_dongle *d, int id);
void		dongle_destroy(t_dongle *d);
int			dongle_acquire(t_dongle *d, t_coder *c, t_sim *sim);
void		dongle_release(t_dongle *d, t_sim *sim);

/* coder.c */
void		*coder_routine(void *arg);

/* monitor.c */
void		*monitor_routine(void *arg);
int			sim_is_stopped(t_sim *sim);
void		sim_stop(t_sim *sim);

/* cleanup.c */
void		free_sim(t_sim *sim);

#endif
