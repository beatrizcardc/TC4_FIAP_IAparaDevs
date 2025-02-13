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

