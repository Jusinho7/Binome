#include "codexion.h"

static int	is_valid_number(const char *s)
{
	int	i;

	if (!s || s[0] == '\0')
		return (0);
	i = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static long long	str_to_ll(const char *s)
{
	long long	res;
	int			i;

	res = 0;
	i = 0;
	while (s[i])
	{
		res = res * 10 + (s[i] - '0');
		if (res > 1000000000LL)
			res = 1000000000LL;
		i++;
	}
	return (res);
}

static int	check_numeric_args(char **argv)
{
	int	i;

	i = 1;
	while (i <= 7)
	{
		if (!is_valid_number(argv[i]))
			return (0);
		i++;
	}
	return (1);
}

static int	parse_scheduler(const char *s, t_sim *sim)
{
	if (strcmp(s, "fifo") == 0)
		sim->scheduler = SCHED_FIFO_MODE;
	else if (strcmp(s, "edf") == 0)
		sim->scheduler = SCHED_EDF_MODE;
	else
		return (0);
	return (1);
}

int	parse_args(int argc, char **argv, t_sim *sim)
{
	if (argc != 9)
		return (0);
	if (!check_numeric_args(argv))
		return (0);
	sim->n_coders = (int)str_to_ll(argv[1]);
	sim->time_to_burnout = str_to_ll(argv[2]);
	sim->time_to_compile = str_to_ll(argv[3]);
	sim->time_to_debug = str_to_ll(argv[4]);
	sim->time_to_refactor = str_to_ll(argv[5]);
	sim->n_compiles_required = (int)str_to_ll(argv[6]);
	sim->dongle_cooldown = str_to_ll(argv[7]);
	if (sim->n_coders < 1 || sim->time_to_burnout <= 0)
		return (0);
	if (!parse_scheduler(argv[8], sim))
		return (0);
	return (1);
}
