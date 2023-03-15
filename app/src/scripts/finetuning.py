import sqlalchemy.orm as _orm
import services as _services

import pickle

from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses
from torch.utils.data import DataLoader
from scripts.preprocessing import make_embeddings_corpus, read_corpus
from scripts.utils import check_time, set_timer, get_new_name
from shutil import move

from rich.console import Console
from rich.panel import Panel


@check_time(repeat = True)
def finetune_model(db: _orm.Session, model, model_path):
    console = Console()

    # Un joli print
    panel = Panel.fit(
        f"[bold magenta]Fine-tuning ...[/bold magenta]",
        title="[bold white]DEBUT DE FINETUNING HEBDOMADAIRE[/bold white]",
        border_style="bold white",
        padding=(1, 2),
    )

    # Print the panel to the console
    console.print(panel)
    # Récupération des données de la BDD
    # Et mise en forme dans le bon format pour l'entraînement
    train_examples = _services.get_data_for_FT(db=db)
    train_dataset = SentencesDataset(train_examples, model)

    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)

    archived_model = get_new_name("sentence_similarity_model_FT", "../models/archive")
    move(f"{model_path}/sentence_similarity_model_FT", archived_model)

    # Entrainement du modèle
    model.fit(train_objectives=[(train_dataloader, train_loss)],
              epochs=3,
              warmup_steps=100)

    # Sauvegarde du modèle
    model.save(f"{model_path}/sentence_similarity_model_FT")

    # Recréation des embeddings avec le nouveau modèle fine-tuné sur les reviews
    corpus = read_corpus("../../Data/movie_synopsis.csv")
    embeddings_FT_corpus_movie = make_embeddings_corpus(corpus=corpus, model=model)

    # Sauvegarde des embeddings
    with open("../embeddings/embeddings_FT_corpus_movie", "wb") as embeddings_file:
        pickle.dump(embeddings_FT_corpus_movie, file=embeddings_file)

    return {
        "message": "modèle fine-tuné"
    }
