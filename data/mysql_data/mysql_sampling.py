import pandas as pd


def shrink_files(folder, publication_file, faculty_pub_file, sample_fraction):
    """
    Shrink the publication and faculty_publication files by sampling a fraction of publications
    and filtering relationships accordingly.

    Args:
        publication_file (str): Path to the publication CSV file.
        faculty_pub_file (str): Path to the faculty_publication CSV file.
        sample_fraction (float): Fraction of publications to sample (default: 1/4).
    """
    # Step 1: Sample publications
    publications = pd.read_csv(publication_file)
    sampled_publications = publications.sample(frac=sample_fraction, random_state=42)  # Fixed random state for reproducibility
    sampled_publications.to_csv(f'{folder}/publication_mini.csv', index=False)
    print(f"Saved sampled publications to 'publication_mini.csv' (rows: {len(sampled_publications)})")

    # Step 2: Filter faculty_publication relationships
    faculty_pub = pd.read_csv(faculty_pub_file)
    sampled_pub_ids = set(sampled_publications['id'])
    faculty_pub_mini = faculty_pub[faculty_pub['publications'].isin(sampled_pub_ids)]
    faculty_pub_mini.to_csv(f'{folder}/faculty_publication_mini.csv', index=False)
    print(f"Saved filtered faculty-publication relationships to 'faculty_publication_mini.csv' (rows: {len(faculty_pub_mini)})")

    # Step 3: Filter publication_keyword relationships
    publication_keyword = pd.read_csv(f'{folder}/publicationhas.csv')
    sampled_pub_ids = set(sampled_publications['id'])
    publication_keyword_mini = publication_keyword[publication_keyword['id'].isin(sampled_pub_ids)]
    publication_keyword_mini.to_csv(f'{folder}/publicationhas_mini.csv', index=False)
    print(f"Saved filtered publication-keyword relationships to 'publicationhas_mini.csv' (rows: {len(publication_keyword_mini)})")


def main():
    folder = 'data/mysql_data/'
    shrink_files(folder, f'{folder}/publication.csv', f'{folder}/facultypublication.csv', sample_fraction=0.90)

if __name__ == "__main__":
    main()
