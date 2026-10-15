NAME		= codexion
CC			= cc
CFLAGS		= -Wall -Wextra -Werror -pthread
INC			= -Iincludes

SRC_DIR		= src
OBJ_DIR		= obj
SRCS		= main.c parse.c init.c cleanup.c run.c coder.c monitor.c \
			  dongle.c dongle_pair.c queue.c fifo_scheduler.c \
			  edf_scheduler.c state.c time_utils.c
OBJS		= $(addprefix $(OBJ_DIR)/, $(SRCS:.c=.o))
HEADER		= includes/codexion.h

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c $(HEADER)
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INC) -c $< -o $@

clean:
	rm -rf $(OBJ_DIR)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
