/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/27 19:43:17 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/27 19:43:20 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_list	*stack_a;
	char	**args;
	int		split;
	t_algo	algo;

	split = 0;
	stack_a = NULL;
	if (argc == 1)
		return (0);
	algo = search_flag(&argc, argv);
	if (argc == 2)
	{
		if (!argv[1] || is_blank(argv[1]))
			ft_error(&stack_a);
		args = ft_split(argv[1], ' ');
		split = 1;
	}
	else
		args = argv + 1;
	ft_parse(&stack_a, args);
	sort(&stack_a, algo);
	ft_free(&stack_a);
	if (split)
		ft_free_split(args);
	return (0);
}
