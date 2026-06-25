#!/usr/bin/env python3
"""Search arXiv for the ForestNav path-quality literature corpus."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "1_survey" / "papers" / "paper_list.csv"
ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
USER_AGENT = "ForestNav literature corpus builder (mailto:research@example.com)"
ACCEPTED_CATEGORIES = {"cs.RO", "cs.AI", "cs.CG", "cs.SY", "cs.MA"}
MIN_TITLE_KEYWORD_HITS = 2


@dataclass(frozen=True)
class PaperSeed:
    arxiv_id: str
    title: str
    year: int
    authors_short: str
    direction_tag: str


DIRECTION_QUERIES: list[tuple[str, str]] = [
    ("A_path_smoothing", "path smoothing nonholonomic vehicle"),
    ("A_path_smoothing", "curvature-constrained path smoothing"),
    ("A_path_smoothing", "shortcutting algorithm motion planning"),
    ("A_path_smoothing", "B-spline path smoothing mobile robot"),
    ("A_path_smoothing", "path smoothing elastic strip post-processing"),
    ("A_path_smoothing", "path shortening algorithm robot"),
    ("A_path_smoothing", "gradient descent path smoothing"),
    ("A_path_smoothing", "conjugate gradient smoothing trajectory"),
    ("A_path_smoothing", "iterative path refinement mobile robot"),
    ("B_trajectory_optimization", "CHOMP trajectory optimization"),
    ("B_trajectory_optimization", "STOMP stochastic trajectory optimization"),
    ("B_trajectory_optimization", "TrajOpt sequential convex optimization"),
    ("B_trajectory_optimization", "trajectory optimization cluttered nonholonomic"),
    ("B_trajectory_optimization", "covariant Hamiltonian optimization CHOMP robot"),
    ("B_trajectory_optimization", "stochastic trajectory optimization STOMP manipulation"),
    ("B_trajectory_optimization", "sequential convex optimization trajectory robot"),
    ("B_trajectory_optimization", "ITOMP interleaving trajectory optimization"),
    ("B_trajectory_optimization", "trajectory optimization functional gradient"),
    ("C_elastic_band", "elastic band path planning"),
    ("C_elastic_band", "Timed Elastic Band TEB planner"),
    ("C_elastic_band", "trajectory deformation obstacle avoidance"),
    ("D_asymptotically_optimal_sampling", "RRT* asymptotically optimal"),
    ("D_asymptotically_optimal_sampling", "BIT* batch informed trees"),
    ("D_asymptotically_optimal_sampling", "FMT* fast marching tree"),
    ("D_asymptotically_optimal_sampling", "Informed RRT* heuristic sampling"),
    ("E_bounded_suboptimal_search", "ARA* anytime repairing A*"),
    ("E_bounded_suboptimal_search", "bounded suboptimality search planning"),
    ("E_bounded_suboptimal_search", "D* Lite incremental search"),
    ("F_hybrid_astar", "Hybrid A* path planning improvement"),
    ("F_hybrid_astar", "state lattice motion planning primitive"),
    ("F_hybrid_astar", "Hybrid A* smoothing post-processing"),
    ("G_subgoal_optimization", "subgoal discovery hierarchical planning"),
    ("G_subgoal_optimization", "waypoint optimization path planning"),
    ("G_subgoal_optimization", "intermediate goal selection planning"),
    ("G_subgoal_optimization", "landmark-based planning robotics"),
    ("H_hierarchical_planning", "hierarchical motion planning quality guarantee"),
    ("H_hierarchical_planning", "multi-resolution path planning"),
    ("H_hierarchical_planning", "coarse-to-fine path planning"),
    ("I_corridor_planning", "corridor-based motion planning"),
    ("I_corridor_planning", "safe flight corridor planning"),
    ("I_corridor_planning", "IRIS convex region decomposition"),
    ("I_corridor_planning", "graphs convex sets GCS trajectory"),
    ("J_homotopy_topology", "homotopy class path planning"),
    ("J_homotopy_topology", "topological path planning robot"),
    ("J_homotopy_topology", "path diversity motion planning"),
    ("K_dubins_reeds_shepp", "Dubins path optimization bounded curvature"),
    ("K_dubins_reeds_shepp", "Reeds-Shepp curve planning car-like"),
    ("K_dubins_reeds_shepp", "clothoid path planning vehicle"),
    ("K_dubins_reeds_shepp", "minimum curvature path planning"),
    ("L_learning_path_optimization", "neural motion planning path quality"),
    ("L_learning_path_optimization", "learned trajectory optimization"),
    ("L_learning_path_optimization", "diffusion model path planning"),
    ("L_learning_path_optimization", "imitation learning path planning"),
    ("M_multi_objective_planning", "multi-objective motion planning Pareto"),
    ("M_multi_objective_planning", "bi-criteria path planning length time"),
    ("M_multi_objective_planning", "multi-criteria path planning robot"),
    ("M_multi_objective_planning", "cost quality tradeoff path planning"),
    ("M_multi_objective_planning", "path length smoothness tradeoff planning"),
    ("M_multi_objective_planning", "anytime multi-objective graph search"),
    ("N_path_repair", "path repair local refinement planning"),
    ("N_path_repair", "experience-based motion planning"),
    ("N_path_repair", "lazy PRM evaluation planning"),
    ("O_dense_forest_narrow_passage", "narrow passage motion planning"),
    ("O_dense_forest_narrow_passage", "dense obstacle path planning forest"),
    ("O_dense_forest_narrow_passage", "off-road autonomous path planning"),
    ("O_dense_forest_narrow_passage", "vegetation navigation robot"),
    ("P_nonholonomic_constraints", "Ackermann steering path planning"),
    ("P_nonholonomic_constraints", "kinodynamic planning nonholonomic"),
    ("P_nonholonomic_constraints", "minimum turning radius path planning nonholonomic survey"),
    ("P_nonholonomic_constraints", "car-like robot path planning curvature constraint"),
    ("P_nonholonomic_constraints", "Ackermann kinematic model path generation"),
    ("P_nonholonomic_constraints", "nonholonomic motion planning review survey"),
    ("P_nonholonomic_constraints", "wheeled mobile robot path planning turning"),
    ("Q_informed_sampling", "informed sampling motion planning"),
    ("Q_informed_sampling", "cross-entropy motion planning sampling"),
    ("Q_informed_sampling", "adaptive sampling path planning"),
    ("R_surveys", "motion planning survey robot 2024"),
    ("R_surveys", "sampling-based motion planning survey"),
    ("R_surveys", "search-based planning survey autonomous"),
]


RELEVANCE_KEYWORDS = {
    "path",
    "planning",
    "trajectory",
    "motion",
    "navigation",
    "smoothing",
    "smooth",
    "spline",
    "geodesic",
    "optimization",
    "search",
    "sampling",
    "rrt",
    "prm",
    "roadmap",
    "lattice",
    "heuristic",
    "dubins",
    "reeds",
    "shepp",
    "clothoid",
    "curvature",
    "obstacle",
    "collision",
    "avoidance",
    "corridor",
    "convex",
    "homotopy",
    "topological",
    "kinematic",
    "kinodynamics",
    "kinodynamic",
    "nonholonomic",
    "ackermann",
    "steering",
    "vehicle",
    "elastic",
    "band",
    "subgoal",
    "waypoint",
    "hierarchical",
    "survey",
    "review",
    "narrow",
    "passage",
    "cluttered",
    "off-road",
    "terrain",
    "forest",
    "vegetation",
    "traversab",
    "informed",
    "adaptive",
    "anytime",
    "repair",
    "replan",
    "refinement",
    "diffusion",
    "neural",
    "learning",
    "imitation",
    "autonomous",
    "robot",
    "robotics",
    "mobile",
    "manipulator",
    "generation",
    "postprocessing",
    "shortening",
}


SEED_PAPERS: list[PaperSeed] = [
    PaperSeed(
        "1601.06326",
        "Practical Search Techniques in Path Planning for Autonomous Driving",
        2016,
        "Dolgov et al.",
        "F_hybrid_astar",
    ),
    PaperSeed(
        "1105.1186",
        "Sampling-based algorithms for optimal motion planning",
        2011,
        "Karaman and Frazzoli",
        "D_asymptotically_optimal_sampling",
    ),
    PaperSeed(
        "1405.5848",
        "Batch Informed Trees BIT*",
        2014,
        "Gammell et al.",
        "D_asymptotically_optimal_sampling",
    ),
    PaperSeed(
        "1404.2334",
        "Informed RRT*",
        2014,
        "Gammell et al.",
        "Q_informed_sampling",
    ),
    PaperSeed(
        "1306.3532",
        "FMT* A Fast Marching Tree Algorithm",
        2013,
        "Janson et al.",
        "D_asymptotically_optimal_sampling",
    ),
    PaperSeed(
        "2002.06599",
        "Adaptively Informed Trees AIT* and EIT*",
        2020,
        "Strub and Gammell",
        "Q_informed_sampling",
    ),
    PaperSeed(
        "1706.09068",
        "Integrated online trajectory planning and optimization in distinctive topologies",
        2017,
        "Roesmann et al.",
        "C_elastic_band",
    ),
    PaperSeed(
        "1310.3163",
        "Finding Locally Optimal Collision-Free Trajectories with Sequential Convex Optimization",
        2013,
        "Schulman et al.",
        "B_trajectory_optimization",
    ),
    PaperSeed(
        "2101.11565",
        "Shortest Paths in Graphs of Convex Sets",
        2021,
        "Marcucci et al.",
        "I_corridor_planning",
    ),
    PaperSeed(
        "1901.03922",
        "Computing Large Convex Regions of Obstacle-Free Space via Semidefinite Programming",
        2019,
        "Deits and Tedrake",
        "I_corridor_planning",
    ),
    PaperSeed(
        "1104.2800",
        "Identifying Homotopy Classes of Trajectories",
        2011,
        "Bhatt et al.",
        "J_homotopy_topology",
    ),
    PaperSeed(
        "1804.07537",
        "Classification of the Dubins set",
        2018,
        "Shkel and Lumelsky",
        "K_dubins_reeds_shepp",
    ),
    PaperSeed(
        "1510.08636",
        "Experience-based Planning with Sparse Roadmap Spanners",
        2015,
        "Coleman et al.",
        "N_path_repair",
    ),
    PaperSeed(
        "2010.15394",
        "Kilometer-scale autonomous navigation in subarctic forests",
        2021,
        "Frey et al.",
        "O_dense_forest_narrow_passage",
    ),
    PaperSeed(
        "1710.00567",
        "Online Safe Trajectory Generation For Quadrotors",
        2018,
        "Gao et al.",
        "I_corridor_planning",
    ),
]


@dataclass
class PaperRow:
    arxiv_id: str
    title: str
    year: int
    authors_short: str
    direction_tag: str


def collapse_ws(text: str) -> str:
    return " ".join(text.split())


def normalize_arxiv_id(entry_id: str) -> str:
    raw = entry_id.rstrip("/").split("/")[-1]
    if "v" in raw:
        base, version = raw.rsplit("v", 1)
        if version.isdigit():
            return base
    return raw


def authors_short(authors: list[str]) -> str:
    if not authors:
        return "Unknown"
    first = collapse_ws(authors[0])
    if len(authors) == 1:
        return first
    return f"{first} et al."


def relevance_hits(title: str) -> set[str]:
    title_lower = title.lower()
    tokens = set(re.findall(r"[a-z0-9]+", title_lower))
    hits: set[str] = set()
    for keyword in RELEVANCE_KEYWORDS:
        if keyword == "traversab":
            if any(token.startswith("traversab") for token in tokens):
                hits.add(keyword)
            continue
        if keyword in tokens:
            hits.add(keyword)
        elif len(keyword) >= 6 and keyword in title_lower:
            hits.add(keyword)
    return hits


def is_title_relevant(title: str, min_hits: int = MIN_TITLE_KEYWORD_HITS) -> bool:
    return len(relevance_hits(title)) >= min_hits


def parse_entries(
    payload: bytes,
    direction_tag: str,
    start_year: int,
    end_year: int,
    min_title_keyword_hits: int,
) -> list[PaperRow]:
    root = ET.fromstring(payload)
    rows: list[PaperRow] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        entry_id_node = entry.find("atom:id", ARXIV_NS)
        title_node = entry.find("atom:title", ARXIV_NS)
        published_node = entry.find("atom:published", ARXIV_NS)
        categories = {
            cat.attrib.get("term", "")
            for cat in entry.findall("atom:category", ARXIV_NS)
        }
        if not (categories & ACCEPTED_CATEGORIES):
            continue
        if entry_id_node is None or title_node is None or published_node is None:
            continue
        title = collapse_ws(title_node.text or "")
        try:
            year = int(published_node.text[:4])
        except (TypeError, ValueError):
            continue
        if year < start_year or year > end_year:
            continue
        hits = relevance_hits(title)
        if len(hits) < min_title_keyword_hits:
            print(
                f"  - skip low-title-relevance hits={len(hits)} categories={','.join(sorted(categories))}: {title}",
                flush=True,
            )
            continue
        authors = [
            author.findtext("atom:name", default="", namespaces=ARXIV_NS)
            for author in entry.findall("atom:author", ARXIV_NS)
        ]
        rows.append(
            PaperRow(
                arxiv_id=normalize_arxiv_id(entry_id_node.text or ""),
                title=title,
                year=year,
                authors_short=authors_short(authors),
                direction_tag=direction_tag,
            )
        )
    return rows


def keyword_terms(keyword: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9]+", keyword)
    return [term for term in terms if len(term) > 1]


def build_search_query(keyword: str) -> str:
    # Keep query recall in title/abstract, then enforce arXiv category and title
    # relevance locally. This avoids all-field hits from bibliography noise.
    terms = keyword_terms(keyword)
    if not terms:
        return "all:robot"
    return " AND ".join(f"(ti:{term} OR abs:{term})" for term in terms)


def fetch_query(keyword: str, max_results: int, timeout: int) -> bytes:
    params = {
        "search_query": build_search_query(keyword),
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def merge_rows(existing: OrderedDict[str, PaperRow], new_rows: list[PaperRow]) -> None:
    for row in new_rows:
        if not row.arxiv_id:
            continue
        previous = existing.get(row.arxiv_id)
        if previous is None:
            existing[row.arxiv_id] = row
            continue
        tags = previous.direction_tag.split(";")
        if row.direction_tag not in tags:
            previous.direction_tag = f"{previous.direction_tag};{row.direction_tag}"


def validate_seed(seed: PaperSeed, timeout: int) -> bool:
    url = f"https://arxiv.org/abs/{seed.arxiv_id}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400
    except Exception as exc:  # noqa: BLE001 - seed validation should not kill the corpus build.
        print(f"  ! skip seed arXiv:{seed.arxiv_id}: HEAD failed: {exc}", file=sys.stderr, flush=True)
        return False


def merge_seed_papers(rows_by_id: OrderedDict[str, PaperRow], timeout: int, sleep: float) -> None:
    print(f"Validating {len(SEED_PAPERS)} seed papers...", flush=True)
    for index, seed in enumerate(SEED_PAPERS, start=1):
        if validate_seed(seed, timeout):
            merge_rows(
                rows_by_id,
                [
                    PaperRow(
                        arxiv_id=seed.arxiv_id,
                        title=seed.title,
                        year=seed.year,
                        authors_short=seed.authors_short,
                        direction_tag=seed.direction_tag,
                    )
                ],
            )
            print(f"  + seed [{index}/{len(SEED_PAPERS)}] arXiv:{seed.arxiv_id}", flush=True)
        if index < len(SEED_PAPERS):
            time.sleep(sleep)


def print_direction_distribution(rows: list[PaperRow]) -> None:
    counts: Counter[str] = Counter()
    for row in rows:
        for tag in row.direction_tag.split(";"):
            counts[tag] += 1
    print("Direction distribution:", flush=True)
    for tag, count in sorted(counts.items()):
        print(f"  {tag}: {count}", flush=True)


def write_csv(rows: list[PaperRow], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["arxiv_id", "title", "year", "authors_short", "direction_tag"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "arxiv_id": row.arxiv_id,
                    "title": row.title,
                    "year": row.year,
                    "authors_short": row.authors_short,
                    "direction_tag": row.direction_tag,
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--sleep", type=float, default=3.0)
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2026)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--min-title-keyword-hits", type=int, default=MIN_TITLE_KEYWORD_HITS)
    parser.add_argument("--no-seed-papers", action="store_true")
    parser.add_argument(
        "--limit-queries",
        type=int,
        default=None,
        help="Only run the first N keyword queries; useful for smoke tests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queries = DIRECTION_QUERIES[: args.limit_queries] if args.limit_queries else DIRECTION_QUERIES
    rows_by_id: OrderedDict[str, PaperRow] = OrderedDict()

    for index, (direction_tag, keyword) in enumerate(queries, start=1):
        print(f"[{index}/{len(queries)}] {direction_tag}: {keyword}", flush=True)
        try:
            payload = fetch_query(keyword, args.max_results, args.timeout)
            rows = parse_entries(
                payload,
                direction_tag,
                args.start_year,
                args.end_year,
                args.min_title_keyword_hits,
            )
        except Exception as exc:  # noqa: BLE001 - keep long corpus jobs moving.
            print(f"  ! query failed: {exc}", file=sys.stderr, flush=True)
            rows = []
        merge_rows(rows_by_id, rows)
        print(f"  + fetched={len(rows)} unique_total={len(rows_by_id)}", flush=True)
        if index < len(queries):
            time.sleep(args.sleep)

    if not args.no_seed_papers:
        merge_seed_papers(rows_by_id, args.timeout, args.sleep)

    rows_out = sorted(rows_by_id.values(), key=lambda row: (-row.year, row.arxiv_id))
    write_csv(rows_out, args.output)
    print(f"Wrote {len(rows_out)} unique papers to {args.output}")
    print_direction_distribution(rows_out)
    if args.limit_queries:
        return 0
    if len(rows_out) < 250:
        print(
            f"WARNING: only {len(rows_out)} rows; target is >=250.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
