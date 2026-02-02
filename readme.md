# 📖 BibleApp 

Um assistente de leitura e anotações bíblicas que une a performance bruta do **C++** na interface de terminal com a flexibilidade do **Python** no processamento de dados e integração com nuvem.



---

## 🛠️ A Arquitetura (O "Pulo do Gato")

Diferente de aplicações comuns, este projeto utiliza uma arquitetura híbrida de alto desempenho:

* **Frontend (C++20):** 
Uma interface de terminal (TUI) desenvolvida em C++ para garantir latência zero, controle total do cursor e manipulação direta de sequências ANSI.

* **The Bridge (Nanobind):** 
Uma camada de vinculação ultra-leve que expõe as funções de interface do C++ como um módulo nativo para o Python.

* **Backend (Python 3.12+):** 
Gerencia a persistência em **SQLite3**, a lógica de busca de versículos e o sistema de ingestão remota via **Telegram Bot API**.

---

## 🚀 Funcionalidades Principais

* **Interface Minimalista:** Foco total no texto, sem distrações visuais.
* **Ingestão Híbrida:** Anote diretamente pelo terminal no PC ou envie insights rápidos pelo celular via Telegram (Long Polling).
* **Busca Reativa:** Visualização instantânea de versículos ao digitar referências (Ex: `GEN 1:1`).
* **Persistência ACID:** Armazenamento seguro em SQLite, garantindo que suas reflexões nunca sejam corrompidas.

---

## 🌟 Por que C++ + Python?

Acreditamos que a melhor ferramenta é aquela que não te limita. O **C++** nos dá a precisão necessária para construir uma interface de usuário rica e responsiva no terminal, enquanto o **Python** nos permite iterar rapidamente em funcionalidades de rede e banco de dados que seriam excessivamente verbosas em linguagens de baixo nível.