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
    sampled_pub_ids = set(sampled_publications['id:ID'])  # Assuming 'id:ID' is the column name
    faculty_pub_mini = faculty_pub[faculty_pub[':END_ID'].isin(sampled_pub_ids)]
    faculty_pub_mini.to_csv(f'{folder}/faculty_publication_mini.csv', index=False)
    print(f"Saved filtered faculty-publication relationships to 'faculty_publication_mini.csv' (rows: {len(faculty_pub_mini)})")

def main():
    folder = 'data/neo4j_data/'
    shrink_files(folder, f'{folder}/publication.csv', f'{folder}/faculty_publication.csv', sample_fraction=0.25)

if __name__ == "__main__":
    main()
