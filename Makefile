# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/22 16:57:42 by srasolov          #+#    #+#              #
#    Updated: 2026/02/03 18:14:43 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libft.a
CC = cc
CFLAGS = -Wall -Werror -Wextra

SRC = ft_atoi.c\
	  ft_bzero.c\
	  ft_calloc.c\
	  ft_isalnum.c\
	  ft_isalpha.c\
	  ft_isascii.c\
	  ft_isdigit.c\
	  ft_isprint.c\
	  ft_memchr.c\
	  ft_memcmp.c\
	  ft_memmove.c\
	  ft_memset.c\
	  ft_memcpy.c\
	  ft_strchr.c\
	  ft_strdup.c\
	  ft_strjoin.c\
	  ft_strlcat.c\
	  ft_strlcpy.c\
	  ft_strlen.c\
	  ft_strncmp.c\
	  ft_strnstr.c\
	  ft_strrchr.c\
	  ft_strtrim.c\
	  ft_split.c\
	  ft_substr.c\
	  ft_tolower.c\
	  ft_toupper.c\
	  ft_strtrim.c\
	  ft_strmapi.c\
	  ft_striteri.c\
	  ft_itoa.c\
	  ft_putchar_fd.c\
	  ft_putstr_fd.c\
	  ft_putendl_fd.c\
	  ft_putnbr_fd.c\
	  ft_lstnew.c\
	  ft_lstadd_front.c\
	  ft_lstsize.c\
	  ft_lstlast.c\
	  ft_lstadd_back.c\
	  ft_lstdelone.c\
	  ft_lstclear.c\
	  ft_lstiter.c\
	  ft_lstmap.c

OBJ = ${SRC:.c=.o}

all: $(NAME)

$(NAME): $(OBJ)
	ar -rcs $@ $^

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY : all fclean clean re