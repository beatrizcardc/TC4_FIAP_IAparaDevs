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

  - ✋ Mão Esquerda Levantada
  - ✋ Mão Direita Levantada
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

 ┗ 📜 Relatório           # Relatório Final
   - https://github.com/beatrizcardc/TC4_FIAP_IAparaDevs/blob/main/emotions_activities_report_fdetection49.txt 

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
____________________________________________________________________________________________________________________________________________________________________________________

📚 Lições Aprendidas

🔍 1. Refinamento Contínuo na Detecção Facial
Desafio inicial:
Detectar rostos em condições adversas, como perfis extremos, rostos parcialmente visíveis ou posições inclinadas.

Solução:
Integração do RetinaFace para melhorar a precisão e abrangência da detecção facial, garantindo uma cobertura mais robusta em todas as condições.

Lição:
A escolha do detector certo pode transformar a qualidade da análise, especialmente em vídeos desafiadores.


🎭 2. Análise de Emoções Mais Precisa e Natural
Desafio inicial:
Contabilização frame a frame das emoções, resultando em um excesso de registros e uma análise artificial.

Solução:
Implementação do conceito de evento único com histórico de 15 frames para identificar mudanças de emoções relevantes.

Lição:
Uma análise mais próxima da percepção humana requer filtrar eventos contínuos para evitar detecções redundantes e desnecessárias.


🕺 3. Refinamento na Detecção de Atividades (Dança, Aperto de Mãos, Mãos Levantadas)
Desafio inicial:
Falsos positivos na detecção de atividades, como confundir cabeças próximas com "aperto de mãos" ou movimentos bruscos como "dança".

Solução:
Ajuste criterioso dos parâmetros para melhorar a precisão, incluindo a análise de distância, alinhamento e continuidade dos movimentos antes de registrar uma atividade.

Lição:
A precisão pode ser alcançada combinando várias dimensões do movimento (posição, altura e profundidade), não apenas a detecção básica.


⚠️ 4. Detecção de Anomalias com Critérios Mais Seletivos
Desafio inicial:
Registrar mudanças frequentes como anomalias, resultando em alertas excessivos.

Solução:
Refinamento das regras para considerar uma anomalia apenas quando mais de 8 mudanças ocorrerem em sequência no histórico de emoções, ou quando eventos atípicos persistirem por tempo suficiente.

Lição:
O equilíbrio entre sensibilidade e precisão é fundamental para uma análise confiável.


📊 5. Integração do MediaPipe para Detecção de Postura e Atividades Corporais
Desafio inicial:
Identificar atividades corporais complexas usando apenas bibliotecas limitadas.

Solução:
Utilização do MediaPipe Pose para análise detalhada das posturas e movimentos corporais, proporcionando uma base sólida para detectar atividades como "dançar" ou "levantar as mãos".

Lição:
Ferramentas específicas para análise corporal enriquecem a interpretação do vídeo e complementam a detecção facial.

______________________________________________________________________________________________________________________________________________________________________________________
🛠️ Principais Desafios Superados
- Integração de múltiplas bibliotecas (FER, RetinaFace, MediaPipe) para garantir uma análise holística e precisa.
- Redução de falsos positivos em atividades corporais como "dança" e "aperto de mãos".
- Otimização do relatório automático, ajustando para exibir eventos únicos e eliminar redundâncias.
- Geração de vídeos com legendas e frames destacados salvos como jpg, facilitando a compreensão visual das análises realizadas.
