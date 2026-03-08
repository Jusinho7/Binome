/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 07:02:27 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/06 11:27:25 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdio.h>

/*int main(void)
{
    t_list *stack_a = NULL;
    t_list *stack_b = NULL;
    t_list *temp;

    t_list * a = ft_new_node(24);
    ft_lstadd_back(&stack_a, a);
    a = ft_new_node(232);
    ft_lstadd_back(&stack_a, a);
    a = ft_new_node(-1);
    ft_lstadd_back(&stack_a, a);
    a = ft_new_node(52);
    ft_lstadd_back(&stack_a, a);
    a = ft_new_node(20);
    ft_lstadd_back(&stack_a, a);
    a = ft_new_node(8);
    ft_lstadd_back(&stack_a, a);

    a = ft_new_node(200);
    ft_lstadd_back(&stack_b, a);
    a = ft_new_node(100);
    ft_lstadd_back(&stack_b, a);
      a = ft_new_node(140);
    ft_lstadd_back(&stack_b, a);
      a = ft_new_node(5);
    ft_lstadd_back(&stack_b, a);
      a = ft_new_node(15);
    ft_lstadd_back(&stack_b, a);
    printf("We print stack a: \n");
    push_a(&stack_b, &stack_a);
    while (stack_a)
    {
        printf("%d\n",stack_a->value);
        temp = stack_a;
        stack_a = stack_a->next;
        free(temp);
    }
    printf("We print stack b: \n");
    while (stack_b)
    {
        printf("%d\n",stack_b->value);
        temp = stack_b;
        stack_b = stack_b->next;
        free(temp);
    }
    return 0;
}*/

int main(int argc, char **argv)
{
    int i;
    int num[argc - 1];
    long  val;
  
    i = 1;
    while (i < argc)
    {
        val = ft_atol(argv[i]);
        if (val > INT_MAX || val < INT_MIN)
        {
          write(1, "error1\n", 7);
          return (1);
        }
        num[i - 1] = (int)val; 
        if (check_doublon(num, i))
        {
          write(1, "error2\n", 7);
          return (1);
        }
        printf("%d ", num[i - 1]);
        i++;
    }
    printf("\n");
    return (0);
}
