import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
AI_KNOWLEDGE_PATH = DATA_DIR / "processed" / "ai_knowledge_base.json"

AI_CONCEPTS: List[Dict] = [
    {
        "id": "KB-AI-01",
        "title": "What is Artificial Intelligence (AI)?",
        "text": "Artificial Intelligence is the branch of computer science focused on creating systems capable of performing tasks that typically require human intelligence. These tasks include problem-solving, pattern recognition, learning from experience, language comprehension, and decision making under uncertainty.",
        "category": "Fundamentals"
    },
    {
        "id": "KB-AI-02",
        "title": "What is Machine Learning (ML)?",
        "text": "Machine Learning is a subset of artificial intelligence that gives computer systems the ability to learn and improve automatically from data without being explicitly programmed. It primarily focuses on algorithms that discover hidden patterns in training data to make accurate predictions on unseen data.",
        "category": "Fundamentals"
    },
    {
        "id": "KB-AI-03",
        "title": "What is Deep Learning?",
        "text": "Deep Learning is a specialized subfield of machine learning based on artificial neural networks with multiple layers (deep architectures). Deep learning models excel at representation learning, automatically extracting high-level hierarchical features from raw sensory inputs like images, audio, and text.",
        "category": "Deep Learning"
    },
    {
        "id": "KB-AI-04",
        "title": "What is Natural Language Processing (NLP)?",
        "text": "Natural Language Processing (NLP) is the multidisciplinary field combining computational linguistics, computer science, and machine learning to enable computers to read, analyze, interpret, and generate human language in a meaningful and contextual manner.",
        "category": "NLP"
    },
    {
        "id": "KB-AI-05",
        "title": "What is a Neural Network?",
        "text": "An artificial neural network is a computational model inspired by the biological neural structures of the human brain. It consists of interconnected artificial neurons organized in layers: an input layer, one or more hidden layers, and an output layer, which compute weighted sums followed by non-linear activation functions.",
        "category": "Neural Networks"
    },
    {
        "id": "KB-AI-06",
        "title": "What is a Transformer Neural Network?",
        "text": "A Transformer is a deep learning architecture introduced in the landmark paper 'Attention Is All You Need' that relies entirely on self-attention mechanisms to compute representations of input sequences in parallel, dispensing with recurrent and convolutional operations. Transformers are the foundation of modern Large Language Models like GPT, BERT, and Claude.",
        "category": "Architectures"
    },
    {
        "id": "KB-AI-07",
        "title": "What is the Self-Attention Mechanism?",
        "text": "Self-attention is an architectural mechanism that allows a neural model to weigh the importance of different tokens in a sequence relative to every other token. It operates by mapping queries, keys, and values to calculate attention weights, enabling models to capture long-range contextual dependencies effectively.",
        "category": "Architectures"
    },
    {
        "id": "KB-AI-08",
        "title": "What is Supervised Learning?",
        "text": "Supervised learning is the machine learning paradigm where an algorithm trains on labeled datasets containing pairs of input features and desired ground-truth target outputs. The model iteratively adjusts its internal parameters to minimize the loss between predicted outputs and real targets.",
        "category": "Paradigm"
    },
    {
        "id": "KB-AI-09",
        "title": "What is Unsupervised Learning?",
        "text": "Unsupervised learning is a machine learning approach where algorithms analyze and discover intrinsic structures, groupings, or densities within unlabeled datasets without human supervision. Common techniques include k-means clustering, principal component analysis (PCA), and autoencoders.",
        "category": "Paradigm"
    },
    {
        "id": "KB-AI-10",
        "title": "What is Reinforcement Learning (RL)?",
        "text": "Reinforcement learning is a goal-oriented machine learning framework where an autonomous agent learns optimal decision-making policies through trial-and-error interactions with an environment, guided by numerical reward or penalty signals to maximize cumulative expected return.",
        "category": "Paradigm"
    },
    {
        "id": "KB-AI-11",
        "title": "What are Generative Adversarial Networks (GANs)?",
        "text": "Generative Adversarial Networks are deep learning frameworks where two neural networks—a generator and a discriminator—compete in a minimax game. The generator synthesizes realistic data samples from random noise, while the discriminator learns to distinguish synthetic samples from real training examples.",
        "category": "Generative AI"
    },
    {
        "id": "KB-AI-12",
        "title": "What is Overfitting and How Can It Be Prevented?",
        "text": "Overfitting occurs when a machine learning model learns the statistical noise, idiosyncrasies, and specific details of the training data too closely, harming its generalization performance on new, unseen data. It is mitigated using techniques such as dropout, L1/L2 weight regularization, data augmentation, early stopping, and cross-validation.",
        "category": "Optimization"
    },
    {
        "id": "KB-AI-13",
        "title": "What is Gradient Descent and Backpropagation?",
        "text": "Gradient descent is a first-order iterative optimization algorithm used to find the local minimum of a differentiable objective loss function by updating parameters in the opposite direction of the gradient. Backpropagation calculates these gradients efficiently using the chain rule of calculus throughout the layers of a neural network.",
        "category": "Optimization"
    },
    {
        "id": "KB-AI-14",
        "title": "What is a Large Language Model (LLM)?",
        "text": "A Large Language Model is an advanced deep learning model with billions of parameters, typically based on decoder-only or encoder-decoder Transformer architectures, trained on massive corpora of text via autoregressive self-supervised next-token prediction to comprehend and generate rich natural language.",
        "category": "Modern AI"
    },
    {
        "id": "KB-AI-15",
        "title": "What is Computer Vision (CV)?",
        "text": "Computer Vision is an interdisciplinary field of artificial intelligence enabling computer systems to perceive, extract, process, and understand visual digital images and videos. Core applications include object detection, semantic image segmentation, facial recognition, and autonomous navigation.",
        "category": "Computer Vision"
    }
]

def init_ai_knowledge_base():
    AI_KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AI_KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
        json.dump(AI_CONCEPTS, f, indent=2)
    return AI_CONCEPTS

def get_ai_concepts() -> List[Dict]:
    if not AI_KNOWLEDGE_PATH.exists():
        return init_ai_knowledge_base()
    with open(AI_KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
