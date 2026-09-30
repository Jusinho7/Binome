NAME		= codexion

CC			= cc
CFLAGS		= -Wall -Wextra -Werror -pthread
RM			= rm -f
THREAD_FLAGS := -pthread

SRCS		= main.c \
			  parsing.c \
			  init.c \
			  cleanup.c \
			  heap.c \
			  heap_utils.c \
			  time_utils.c \
			  log.c \
			  control.c \
			  dongle_wait.c \
			  dongle.c

OBJ_DIR		= obj
OBJS		= $(addprefix $(OBJ_DIR)/, $(SRCS:.c=.o))

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(THREAD_FLAGS) $(OBJS) -o $(NAME)

$(OBJ_DIR)/%.o: %.c codexion.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(THREAD_FLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

clean:
	$(RM) -r $(OBJ_DIR)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re