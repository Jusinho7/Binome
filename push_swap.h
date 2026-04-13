/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/03 19:29:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/13 14:32:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "ft_printf.h"
# include <limits.h>
# include <stddef.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_list
{
	int				value;
	struct s_list	*next;
}					t_list;

typedef enum s_algo
{
	ADAPTIVE,
	SIMPLE,
	MEDIUM,
	COMPLEX
}					t_algo;

typedef struct s_counters
{
	int				sa;
	int				sb;
	int				ss;
	int				pa;
	int				pb;
	int				ra;
	int				rb;
	int				rr;
	int				rra;
	int				rrb;
	int				rrr;
}					t_counters;

typedef struct s_options
{
	int				bench_mode;
	t_counters		counters;
}					t_options;

typedef struct s_chunk
{
	int				*ranks;
	int				min;
	int				max;
	int				size;
	int				chunk_size;
}					t_chunk;

typedef struct s_radix
{
	int				bit;
	int				size;
	int				bits;
}					t_radix;

typedef struct s_ctx
{
	t_list			*stack_a;
	t_list			*stack_b;
	char			**args;
	int				split;
	t_options		opts;
	int				disorder;
	int				n;
	t_algo			algo;
	t_algo			used_algo;
}					t_ctx;

typedef struct s_bench
{
	double			disorder;
	double			perc;
	int				n;
	t_algo			algo;
}					t_bench;

t_list				*ft_lst_last(t_list *lst);
void				reverse_a(t_list **stack_a, int bench_mode,
						t_counters *counters);
void				reverse_b(t_list **stack_b, int bench_mode,
						t_counters *counters);
void				reverse_all(t_list **stack_a, t_list **stack_b,
						int bench_mode, t_counters *counters);
void				rotate_a(t_list **stack_a, int bench_mode,
						t_counters *counters);
void				rotate_b(t_list **stack_b, int bench_mode,
						t_counters *counters);
void				rotate_all(t_list **stack_a, t_list **stack_b,
						int bench_mode, t_counters *counters);
void				swap_a(t_list **stack_a, int bench_mode,
						t_counters *counters);
void				swap_b(t_list **stack_b, int bench_mode,
						t_counters *counters);
void				swap_all(t_list **stack_a, t_list **stack_b, int bench_mode,
						t_counters *counters);
void				push_a(t_list **stack_b, t_list **stack_a, int bench_mode,
						t_counters *counters);
void				push_b(t_list **stack_a, t_list **stack_b, int bench_mode,
						t_counters *counters);
t_list				*ft_new_node(int value);
void				ft_lstadd_back(t_list **lst, t_list *new);

void				ft_parse(t_list **stack_a, char **argv);
int					check_doublon(int *num, int len);
long				ft_atol(const char *nptr);
int					count_arg(char **args);
char				**ft_split(char const *s, char c);
void				ft_free_split(char **args);
int					ft_isnumber(char *str);
int					is_blank(char *str);

void				ft_error(t_list **stack);
void				ft_free(t_list **stack);

void				print_bench(int disorder, int n, t_algo algo,
						t_counters *counters);

void				ft_print(t_list *stack, char *name);
int					ft_strcmp(const char *s1, const char *s2);

t_algo				check_flag(char *arg);
int					ft_lstsize(t_list *lst);
int					check_disorder(t_list *stack);
t_algo				detect_algo(t_list *stack);
int					is_sorted(t_list *stack);
t_algo				search_flag(int *argc, char **argv, int *bench_mode);

void				sort(t_list **stack_a, t_algo algo, t_algo *used_algo,
						t_options *opts);
void				sort_simple(t_list **stack_a, t_list **stack_b,
						t_options *opts);
void				sort_medium(t_list **stack_a, t_list **stack_b,
						t_options *opts);
void				sort_complex(t_list **stack_a, t_list **stack_b,
						t_options *opts);
int					get_max_pos(t_list *stack_b);
void				max_to_top_b(t_list **stack_b, t_options *opts);
int					get_max_value(t_list *stack);
int					*get_ranks(t_list *stack_a, int size_a);
int					*save_originals(t_list *stack, int size);
void				restore_values(t_list *stack, int *originals);

#endif
