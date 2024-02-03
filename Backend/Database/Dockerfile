FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=database
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

EXPOSE 3306

COPY ./database.sql /docker-entrypoint-initdb.d/

CMD ["mysqld"]

