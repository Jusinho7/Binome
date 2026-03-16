# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/12 09:24:52 by srasolov          #+#    #+#              #
#    Updated: 2026/03/16 11:06:24 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = push_swap

CC = cc
CFLAGS = -Wall -Wextra -Werror

SRCS =  main.c \
        checker.c \
        check_files.c \
        ft_split.c \
        push.c \
        swap.c \
        rotate.c \
        reverse.c \
        utils.c \
        ft_printf.c \
        ft_putchar.c \
        ft_putstr.c \
        ft_putnbr.c \
        ft_puthex.c \
        ft_putptr.c \
        ft_putunsigned.c\
        ft_strcmp.c \
        check_flags.c

OBJS = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re