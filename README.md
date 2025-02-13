# Tech Challenge - Análise de Vídeo com Reconhecimento Facial e Detecção de Atividades

## Este projeto foi desenvolvido como parte do Tech Challenge da FIAP, com o objetivo de criar uma aplicação que analisa vídeos, detectando rostos, expressões emocionais, atividades corporais e anomalias. A aplicação gera automaticamente um relatório detalhado com os resultados da análise.
____________________________________________________________________________________________________________________________________________________________________________________

### ✨ Funcionalidades Principais

👤 Reconhecimento Facial:

- 📌 Identificação de rostos no vídeo

- 🛠 Utiliza a biblioteca DeepFace com o detector retinaface para detecção precisa de rostos.

😊 Análise de Expressões Emocionais:

- 🔍 Detecta expressões emocionais dos rostos identificados

- 🛠 Utiliza a biblioteca FER (Facial Expression Recognition) para reconhecer emoções como:

  - 😊 Felicidade
  - 😢 Tristeza
  - 😠 Raiva
  - 😨 Medo
  - 😲 Surpresa
___________________________________________________________________________________________________________________________________________________________________________________ 
🏃 Detecção de Atividades Corporais:

- ✋ Detecta atividades como:

  - Mão Esquerda Levantada
  - Mão Direita Levantada
  - 🙌 Mãos Levantadas
  - 💃 Dança
  - 🤝 Aperto de Mãos
    
- 🛠 Baseado no MediaPipe Pose para análise de postura e movimentos.
____________________________________________________________________________________________________________________________________________________________________________________
⚠️ Detecção de Anomalias:

- 🔄 Identifica comportamentos atípicos e mudanças rápidas de emoções
  
- 📈 Detecta anomalias quando há:
  
  - Mudança frequente de emoções em curtos períodos
    
  - Repetição excessiva de uma mesma emoção
 
____________________________________________________________________________________________________________________________________________________________________________________
📝 Geração de Relatório:

- 📊 Resumo Automático:
  - Total de frames analisados
  - Emoções detectadas
  - Atividades identificadas
  - Anomalias encontradas
  - 🖼 Imagens Destacadas:
    
      - Salva frames das atividades e anomalias detectadas para análise posterior

____________________________________________________________________________________________________________________________________________________________________________________
🛠 Tecnologias Utilizadas:

- 📦 OpenCV — Manipulação de vídeo e imagens
- 🎭 MediaPipe — Detecção de pose e reconhecimento de movimentos
- 😄 FER — Análise de expressões faciais
- 🛠 DeepFace — Detecção avançada de rostos
- ⏳ Tqdm — Barra de progresso para processamento de vídeo
- 📈 NumPy — Manipulação eficiente de arrays e dados
____________________________________________________________________________________________________________________________________________________________________________________

📂 Estrutura do Projeto:

📦 projeto

 ┣ 📂 anomaly_frames      # Imagens de anomalias detectadas
 
 ┣ 🎥 Videos:             # Vídeos do Projeto

     - 🎥 https://youtu.be/F2h3tjx8BnQ - Vídeo original do Desafio

     - 🎥 https://youtu.be/RKzE78AzlCY - Vídeo com o Resultado da Identificação Facial

     - 🎥 https://youtu.be/YgX-sOUhNts - Vídeo com o Resultado da Análise de Emoções, Atividades e Anomalias
 
 ┣ 📜 requirements.txt    # Dependências do projeto
 
 ┣ 📜 clean_analysis_notebook.ipynb  # Notebook limpo com a análise
 
 ┗ 📜 README.md           # Descrição do projeto

 ┗ 📜 Relatório

 _____________________________________________________________________________________________________________________________________________________________________________________

## 🔧 Ajustes Realizados e Melhorias no Projeto

🧑‍💻 Refinamento das Técnicas Utilizadas

- Detecção Facial com RetinaFace e MediaPipe:
  - Melhoramos a precisão para garantir a identificação de rostos em perfis extremos e posições incomuns, como pessoas deitadas ou parcialmente ocultas.

- Análise de Emoções com FER:
  - Implementamos a detecção de emoções como felicidade, tristeza, raiva e surpresa.

- Identificação de Anomalias Emocionais:
    - Utilizamos um histórico de 15 frames para analisar mudanças bruscas de emoção, considerando anomalias quando ocorriam mais de 8 mudanças consecutivas.

- Evento Único:
    - Redução da contagem frame a frame, analisando cada evento como um único momento, aproximando a análise ao comportamento humano.
      
🎭 Detecção e Refinamento de Atividades

  - Detecção de Mãos Levantadas, Dança e Aperto de Mãos:
  - Refinamos a lógica para evitar falsos positivos e capturar eventos reais com maior precisão.

- Separação de Frames:

    - Frames das atividades detectadas (dança, aperto de mãos e anomalias) são salvos para refinar e validar manualmente a lógica de detecção, garantindo maior confiabilidade nos resultados.

📈 Relatório e Visualização

- Geração Automática de Relatório:
    - Relatório detalhado com ícones para emoções e atividades, tornando a apresentação clara e visualmente amigável.

- Captura de Frames:
    - Frames de atividades específicas (dança, aperto de mãos) e anomalias são salvos automaticamente para análise posterior.
