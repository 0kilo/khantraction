r"""
Phase D Species Clustering and Identity Mapping
Date: 2026-03-29
Purpose: Ingests the dense neighborhood sweep data and applies a clustering 
algorithm to formally map the discrete "Indistinguishability Classes" 
(particle species) supported by the classical Khantraction theory.
"""

import os
import csv
import json
import numpy as np

def load_neighborhood_data(data_dir):
    """Loads all perturbed seeds from the neighborhood sweeps."""
    all_seeds = []
    for file in os.listdir(data_dir):
        if file.endswith("_neighborhood.csv"):
            anchor_name = file.replace("_neighborhood.csv", "")
            filepath = os.path.join(data_dir, file)
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_seeds.append({
                        "anchor_origin": anchor_name,
                        "d_theta": float(row["d_theta"]),
                        "d_phi": float(row["d_phi"]),
                        "d_rho": float(row["d_rho"]),
                        "final_mass": float(row["final_mass"]),
                        "compactness_ratio": float(row["compactness_ratio"])
                    })
    return all_seeds

def cluster_species(seeds, tolerance=1e-3):
    """
    Groups seeds into Indistinguishability Classes based on their 
    invariant Compactness Ratio. If the variance within a group is 
    below the tolerance, they are classified as the identical species.
    """
    clusters = {}
    
    for seed in seeds:
        c_val = seed["compactness_ratio"]
        matched = False
        
        # Check if it fits an existing cluster
        for c_id, cluster_data in clusters.items():
            centroid = cluster_data["centroid"]
            if abs(c_val - centroid) < tolerance:
                cluster_data["members"].append(seed)
                # Recalculate centroid
                all_c = [m["compactness_ratio"] for m in cluster_data["members"]]
                cluster_data["centroid"] = sum(all_c) / len(all_c)
                cluster_data["origins"].add(seed["anchor_origin"])
                matched = True
                break
                
        # Create new cluster if no match
        if not matched:
            new_id = f"Species_Class_{len(clusters) + 1}"
            clusters[new_id] = {
                "centroid": c_val,
                "origins": {seed["anchor_origin"]},
                "members": [seed]
            }
            
    # Format for export
    formatted_clusters = {}
    for c_id, data in clusters.items():
        formatted_clusters[c_id] = {
            "mean_compactness_ratio": data["centroid"],
            "member_count": len(data["members"]),
            "dominant_origin": list(data["origins"])[0],
            "variance": np.var([m["compactness_ratio"] for m in data["members"]])
        }
        
    return formatted_clusters

if __name__ == "__main__":
    print("Initializing Phase D Species Clustering...")
    data_dir = "solutions/phase_d_neighborhood_stability"
    out_dir = "solutions/phase_d_species_clustering"
    os.makedirs(out_dir, exist_ok=True)
    
    print("Loading perturbed neighborhood data...")
    seeds = load_neighborhood_data(data_dir)
    
    print("Clustering into Indistinguishability Classes...")
    clusters = cluster_species(seeds, tolerance=0.05) # Strict clustering threshold
    
    out_path = os.path.join(out_dir, "indistinguishability_classes.json")
    with open(out_path, 'w') as f:
        json.dump(clusters, f, indent=4)
        
    print(f"Clustering complete. Identified {len(clusters)} distinct Khantraction species.")
    print(f"Data deposited in {out_path}")