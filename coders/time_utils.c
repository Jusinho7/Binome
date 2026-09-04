#include "codexion.h"

long long	get_time_ms(t_sim *sim)
{
	struct timeval	tv;
	long long		ms;

	gettimeofday(&tv, NULL);
	ms = (tv.tv_sec - sim->start_time.tv_sec) * 1000LL;
	ms += (tv.tv_usec - sim->start_time.tv_usec) / 1000LL;
	return (ms);
}

void	sleep_ms(long long ms)
{
	if (ms > 0)
		usleep((useconds_t)(ms * 1000));
}

void	ms_to_abs_timespec(t_sim *sim, long long ms, struct timespec *ts)
{
	long long	total_us;

	total_us = (long long)sim->start_time.tv_sec * 1000000LL;
	total_us += sim->start_time.tv_usec;
	total_us += ms * 1000LL;
	ts->tv_sec = total_us / 1000000LL;
	ts->tv_nsec = (total_us % 1000000LL) * 1000LL;
}
