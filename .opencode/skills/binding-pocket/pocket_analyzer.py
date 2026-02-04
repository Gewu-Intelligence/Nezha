#!/usr/bin/env python3
import argparse
import sys
import os
import numpy as np
import csv
from pathlib import Path

try:
    import pyKVFinder
except ImportError:
    print("Error: pyKVFinder is not installed")
    print("Please install pyKVFinder from: https://github.com/LBC-LNBio/pyKVFinder")
    sys.exit(1)


class PocketAnalyzer:
    def __init__(self, pdb_file):
        self.pdb_file = pdb_file
        self.results = None
        self.pockets = []

    def detect_pockets(self, step=0.6, probe_in=1.4, probe_out=4.0, 
                      removal_distance=2.4, volume_cutoff=5.0,
                      include_depth=True, include_hydropathy=False,
                      verbose=False):
        #try:
        print(f"Detecting pockets in {self.pdb_file}...")
            
        self.results = pyKVFinder.run_workflow(
                input=self.pdb_file,
                step=step,
                probe_in=probe_in,
                probe_out=probe_out,
                removal_distance=removal_distance,
                volume_cutoff=volume_cutoff,
                include_depth=include_depth,
                include_hydropathy=include_hydropathy,
                verbose=verbose
            )
            
        print(f"Detected {self.results.ncav} pockets")
        self.analyze_pockets()
        return True
            
        #except Exception as e:
        #    print(f"Error detecting pockets: {e}")
        #    return False

    def analyze_pockets(self):
        if self.results is None:
            print("No results to analyze")
            return
        
        cavities = self.results.cavities
        vertices = self.results._vertices
        step = self.results._step
        
        # Get unique cavity IDs (skip -1, 0, 1)
        cavity_ids = np.unique(cavities)
        cavity_ids = cavity_ids[cavity_ids > 1]

        # Map cavity label to name (KAA, KAB, KAC, ...)
        def get_cavity_name(label):
            if label < 2:
                return None
            idx = label - 2
            if idx < 26:
                return f"KA{chr(65 + idx)}"
            elif idx < 52:
                return f"KB{chr(65 + (idx - 26))}"
            elif idx < 78:
                return f"KC{chr(65 + (idx - 52))}"
            elif idx < 104:
                return f"KD{chr(65 + (idx - 78))}"
            elif idx < 130:
                return f"KE{chr(65 + (idx - 104))}"
            else:
                return f"K{idx}"
        
        for cavity_id in cavity_ids:
            cavity_name = get_cavity_name(cavity_id)
            
            # Find all points belonging to this cavity
            points = np.where(cavities == cavity_id)
            x_coords = points[0] * step + vertices[0, 0]
            y_coords = points[1] * step + vertices[0, 1]
            z_coords = points[2] * step + vertices[0, 2]
            
            # Calculate center
            center = [
                np.mean(x_coords),
                np.mean(y_coords),
                np.mean(z_coords)
            ]
            
            # Calculate size (bounding box)
            size = [
                np.max(x_coords) - np.min(x_coords),
                np.max(y_coords) - np.min(y_coords),
                np.max(z_coords) - np.min(z_coords)
            ]
            
            # Get volume and area from results
            volume = self.results.volume.get(cavity_name, 0.0) if cavity_name else 0.0
            area = self.results.area.get(cavity_name, 0.0) if cavity_name else 0.0
            
            # Get depth information if available
            max_depth = self.results.max_depth.get(cavity_name, 0.0) if self.results.max_depth and cavity_name else 0.0
            avg_depth = self.results.avg_depth.get(cavity_name, 0.0) if self.results.avg_depth and cavity_name else 0.0
            
            # Get interface residues
            residues = self.results.residues.get(cavity_name, []) if cavity_name else []
            
            pocket = {
                'id': cavity_name,
                'label': cavity_id,
                'center': center,
                'size': size,
                'volume': volume,
                'area': area,
                'max_depth': max_depth,
                'avg_depth': avg_depth,
                'residues': residues,
                'residue_count': len(residues)
            }
            
            self.pockets.append(pocket)
        self.pockets = sorted(self.pockets, key=lambda x:x["volume"], reverse=True)

    def print_results(self):
        if not self.pockets:
            print("No pockets found")
            return

        print("\n" + "="*80)
        print(f"POCKET ANALYSIS RESULTS FOR: {self.pdb_file}")
        print("="*80)
        print(f"\nTotal pockets found: {len(self.pockets)}\n")

        for i, pocket in enumerate(self.pockets, 1):
            print(f"POCKET {i} (ID: {pocket['id']}, Label: {pocket['label']})")
            print("-" * 80)
            print(f"  Center (X, Y, Z):       {pocket['center'][0]:10.3f}  {pocket['center'][1]:10.3f}  {pocket['center'][2]:10.3f} Å")
            print(f"  Size (X, Y, Z):         {pocket['size'][0]:10.3f}  {pocket['size'][1]:10.3f}  {pocket['size'][2]:10.3f} Å")
            print(f"  Volume:                 {pocket['volume']:10.3f} Å³")
            print(f"  Surface Area:           {pocket['area']:10.3f} Å²")
            print(f"  Max Depth:              {pocket['max_depth']:10.3f} Å")
            print(f"  Avg Depth:              {pocket['avg_depth']:10.3f} Å")
            print(f"  Residues ({pocket['residue_count']}):         ", end="")
            
            if pocket['residues']:
                residue_list = []
                for res in pocket['residues']:
                    res_str = f"{res[1]}{res[0]}{res[2]}"
                    residue_list.append(res_str)
                print(", ".join(residue_list[:20]))
                if len(residue_list) > 20:
                    print(f"                          ... and {len(residue_list) - 20} more residues")
            else:
                print("None")
            
            print()

    def export_to_csv(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = [
                'pocket_id', 'pocket_label', 'center_x', 'center_y', 'center_z',
                'size_x', 'size_y', 'size_z', 'volume', 'area',
                'max_depth', 'avg_depth', 'residue_count', 'residues'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for pocket in self.pockets:
                residues_str = ""
                if pocket['residues']:
                    residue_list = []
                    for res in pocket['residues']:
                        res_str = f"{res[1]}{res[0]}{res[2]}"
                        residue_list.append(res_str)
                    residues_str = "; ".join(residue_list)
                
                writer.writerow({
                    'pocket_id': pocket['id'],
                    'pocket_label': pocket['label'],
                    'center_x': pocket['center'][0],
                    'center_y': pocket['center'][1],
                    'center_z': pocket['center'][2],
                    'size_x': pocket['size'][0],
                    'size_y': pocket['size'][1],
                    'size_z': pocket['size'][2],
                    'volume': pocket['volume'],
                    'area': pocket['area'],
                    'max_depth': pocket['max_depth'],
                    'avg_depth': pocket['avg_depth'],
                    'residue_count': pocket['residue_count'],
                    'residues': residues_str
                })
        
        print(f"Results exported to: {output_file}")

    def export_cavity_pdb(self, output_file):
        if self.results is None:
            print("No results to export")
            return
        
        pdb_string = self.results.export(output=output_file)
        print(f"Cavity PDB exported to: {output_file}")

    def get_pockets_summary(self):
        return {
            'total_pockets': len(self.pockets),
            'pockets': self.pockets
        }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze protein pockets using pyKVFinder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
  Examples:
  %(prog)s protein.pdb                                      # Analyze and display results
  %(prog)s protein.pdb -o results.csv                     # Export results to CSV
  %(prog)s protein.pdb --cavity-pdb cavity.pdb            # Export cavity PDB file
  %(prog)s protein.pdb -o results.csv --cavity-pdb c.pdb   # Export both CSV and PDB
  %(prog)s protein.pdb --step 0.5 --volume-cutoff 10.0    # Custom detection parameters
        """
    )
    
    parser.add_argument("pdb_file", help="Input PDB file")
    parser.add_argument("-o", "--output", help="Export results to CSV file")
    parser.add_argument("--cavity-pdb", help="Export cavity points to PDB file")
    parser.add_argument("--no-display", action="store_true", help="Don't display results on screen")
    
    # Detection parameters
    parser.add_argument("--step", type=float, default=0.6, 
                       help="Grid spacing in Å (default: 0.6)")
    parser.add_argument("--probe-in", type=float, default=1.4,
                       help="Probe In size in Å (default: 1.4)")
    parser.add_argument("--probe-out", type=float, default=4.0,
                       help="Probe Out size in Å (default: 4.0)")
    parser.add_argument("--removal-distance", type=float, default=2.4,
                       help="Removal distance from cavity-bulk frontier in Å (default: 2.4)")
    parser.add_argument("--volume-cutoff", type=float, default=5.0,
                       help="Cavities volume filter in Å³ (default: 5.0)")
    parser.add_argument("--no-depth", action="store_true", 
                       help="Don't calculate depth")
    parser.add_argument("--hydropathy", action="store_true",
                       help="Calculate hydropathy")
    
    args = parser.parse_args()

    if not os.path.exists(args.pdb_file):
        print(f"Error: File {args.pdb_file} not found")
        sys.exit(1)

    analyzer = PocketAnalyzer(args.pdb_file)
    
    if analyzer.detect_pockets(
        step=args.step,
        probe_in=args.probe_in,
        probe_out=args.probe_out,
        removal_distance=args.removal_distance,
        volume_cutoff=args.volume_cutoff,
        include_depth=not args.no_depth,
        include_hydropathy=args.hydropathy,
        verbose=False
    ):
        if not args.no_display:
            analyzer.print_results()
        
        if args.output:
            analyzer.export_to_csv(args.output)
        
        if args.cavity_pdb:
            analyzer.export_cavity_pdb(args.cavity_pdb)
        
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
