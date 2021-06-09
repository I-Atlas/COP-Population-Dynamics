from src.animals import Fox, Rabbit, Carrot
from src.population_dynamics import AnimalEvolution
from src.visualization import population_stats_plot, animal_stats_plot
from src.IO_utils import to_file, slugify, ensure_dir, to_json
from datetime import datetime
import numpy as np

fox_density = 0.001
rabbit_density = 0.007
carrot_density = 0.02
map_size = 50
settings = {
    "map_size": map_size,
    "animals": ["fox", "rabbit"],
    "foods": ["carrot", ],
    "fox": int(fox_density * map_size ** 2),
    "rabbit": int(rabbit_density * map_size ** 2),
    "carrot": int(carrot_density * map_size ** 2),
    "food_spawn_chance": {"carrot": 0.0004},
    "stop_at_zero": True,
    "animal_std": 0.1,
    "avoid_extinction": False
}

# map_size = 50
# settings = {
#     "map_size": map_size,
#     "animals": ["fox", "rabbit"],
#     "foods": ["carrot", ],
#     "fox": 2,
#     "rabbit": 4,
#     "carrot": 20,
#     "food_spawn_chance": {"carrot": 0.0001},
#     "stop_at_zero": True,
#     "animal_std": 0,
#     "avoid_extinction": False
# }

fox_inits = {
    "mean_speed": 3,
    "mean_reproductive_drive": 200,
    "mean_sight_radius": 5,
    "mean_max_hunger": 4000,
    "mean_max_age": 10000
}
rabbit_inits = {
    "mean_speed": 2,
    "mean_reproductive_drive": 30,
    "mean_sight_radius": 10,
    "mean_max_hunger": 400,
    "mean_max_age": 4000,
    "nutritional_value": 400
}


# Set up simulation
animal_objects = {"fox": {"object": Fox, "init": fox_inits}, "rabbit": {"object": Rabbit, "init": rabbit_inits}}
food_objects = {"carrot": Carrot}


def run_sim(_settings=settings, id="no_id", basepath="generated/", maxcycles=1000, food_objects=food_objects,
            animal_objects=animal_objects) -> str:
    """Run a simulation and write it to file identified by id."""
    # Set up file structure
    # Cut off folder separator if it is present
    if basepath[-1] == '/' or basepath[-1] == '\\':
        basepath = basepath[:-1]
    # define fpath
    fpath = f"{basepath}/{slugify(datetime.now().isoformat())}-{id}-std{_settings['animal_std']}/"
    ensure_dir(fpath)

    # Write simulation parameters to file
    to_json(fpath + "settings.json", _settings)
    to_json(fpath + "fox_inits.json", fox_inits)
    to_json(fpath + "rabbit_inits.json", rabbit_inits)

    ae = AnimalEvolution(_settings, food_objects, animal_objects)

    # Run the simulation
    stats, genes = ae.run_cycles(maxcycles=maxcycles)

    # Save simulated data
    to_file(fpath + "stats", stats)
    to_file(fpath + "genes", genes)

    # Plot gathered data
    population_stats_plot(stats, food_objects, animal_objects, title=fpath)

    for i, animal in enumerate(animal_objects.keys()):
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(0, 2))
        animal_stats_plot(genes[::, i, ::, ::], title=animal, labels=(2, 9))

    return fpath


if __name__ == "__main__":
    run_sim(settings, basepath="generated/singleruns", maxcycles=10000, id="evolution_largemap")
    # for std in np.linspace(0., .8, 5):
    #     for run_id in range(1):
    #         settings["animal_std"] = std
    #         run_sim(settings, basepath="generated/evolution_run1", maxcycles=50000, id=f"seriousRun-{run_id}")
