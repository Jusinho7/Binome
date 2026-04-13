/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/27 19:43:17 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/12 09:22:17 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	init_context(t_ctx *ctx)
{
	ctx->stack_a = NULL;
	ctx->args = NULL;
	ctx->split = 0;
	ctx->opts.bench_mode = 0;
	ctx->opts.counters = (t_counters){0};
}

static char	**parse_args(int argc, char **argv, int *split, t_list **stack_a)
{
	char	**args;

	*split = 0;
	if (argc == 2)
	{
		if (!argv[1] || is_blank(argv[1]))
			ft_error(stack_a);
		args = ft_split(argv[1], ' ');
		*split = 1;
	}
	else
		args = argv + 1;
	return (args);
}

static void	handle_bench(t_ctx *ctx)
{
	if (ctx->opts.bench_mode)
	{
		ctx->n = ft_lstsize(ctx->stack_a);
		ctx->disorder = check_disorder(ctx->stack_a);
	}
}

static void	print_bench_if_needed(t_ctx *ctx)
{
	if (ctx->opts.bench_mode)
		print_bench(ctx->disorder, ctx->n, ctx->algo, &ctx->opts.counters);
}

int	main(int argc, char **argv)
{
	t_ctx	ctx;

	if (argc == 1)
		return (0);
	init_context(&ctx);
	ctx.algo = search_flag(&argc, argv, &ctx.opts.bench_mode);
	ctx.args = parse_args(argc, argv, &ctx.split, &ctx.stack_a);
	ft_parse(&ctx.stack_a, ctx.args);
	handle_bench(&ctx);
	sort(&ctx.stack_a, ctx.algo, &ctx.used_algo, &ctx.opts);
	print_bench_if_needed(&ctx);
	ft_free(&ctx.stack_a);
	if (ctx.split)
		ft_free_split(ctx.args);
	return (0);
}
