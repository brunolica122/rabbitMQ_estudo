# rabbitMQ_estudo

Esta solução consiste em uma aplicação que monitora um diretório no Linux chamado "arquivos_secretos" e envia mensagens para uma fila no RabbitMQ se ocorrerem mudanças nesse diretório, como modificações, exclusões ou criações de arquivos. Outra aplicação consome essa fila do RabbitMQ e envia as mensagens por SMS para o cliente.
