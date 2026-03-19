/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/19 15:41:25 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/19 16:15:32 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line_bonus.h"

char	*red_line(int fd, char *content)
{
	char	*buf;
	int		read_size;
	char	*tmp;

	buf = malloc(BUFFER_SIZE + 1);
	if (!buf)
		return (0);
	read_size = 1;
	while ((!content || !ft_strchr(content, '\n')) && read_size)
	{
		read_size = read(fd, buf, BUFFER_SIZE);
		if (read_size == -1)
			return (free(buf), free(content), NULL);
		buf[read_size] = '\0';
		if (!content)
			content = ft_strdup(buf);
		else
		{
			tmp = content;
			content = ft_strjoin(tmp, buf);
			free(tmp);
		}
	}
	return (free(buf), content);
}

char	*set_line(char *content)
{
	size_t	i;
	char	*line;

	i = 0;
	if (!content || !content[i])
		return (0);
	while (content[i] && content[i] != '\n')
		i++;
	line = malloc(i + (content[i] == '\n') + 1);
	if (!line)
		return (0);
	i = 0;
	while (content[i] && content[i] != '\n')
	{
		line[i] = content[i];
		i++;
	}
	if (content[i] == '\n')
		line[i++] = '\n';
	line[i] = '\0';
	return (line);
}

char	*get_next_line_bonus(int fd)
{
	char		*line;
	static char	*content[1024];

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (0);
	content[fd] = red_line(fd, content[fd]);
	if (!content[fd])
		return (0);
	line = set_line(content[fd]);
	content[fd] = ft_new_line(content[fd]);
	return (line);
}
