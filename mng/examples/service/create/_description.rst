Neste subcomando você pode criar objetos ``Service`` que pode
ser composto por várias *instâncias* como o **Protheus** ou
apenas está contido em um ``Host`` como o **Nginx**.

Um serviço não tem nenhum campo que se relacione diretamente
com um outro objeto, isso signfica dizer que você deve usar os
outros objetos para ter um relacionamento ``1-N``. Exemplo,
uma *instância* tem um camplo chamado ``service`` que aponta para
um *serviço*.