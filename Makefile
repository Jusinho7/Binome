NAME = codexion

CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread

SRC_DIR = coders
SRCS = main.c parsing.c init.c dongle.c coder.c monitor.c log_utils.c time_utils.c cleanup.c
OBJS = $(addprefix $(SRC_DIR)/, $(SRCS:.c=.o))
HEADER = $(SRC_DIR)/codexion.h

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(SRC_DIR)/%.o: $(SRC_DIR)/%.c $(HEADER)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
