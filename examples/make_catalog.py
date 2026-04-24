import pandas as pd

df0 = pd.DataFrame(
    {
        "obj_id": ["ss_0", "ss_1", "ss_2", "ss_3"],
        "ra": [65.1232370, 65.0446390, 65.1515660, 65.2045730],
        "dec": [-33.4668235, -33.4977818, -33.5285248, -33.4125289],
        "magnorm": [17.5, 17.5, 17.3, 17.3],
        "sed_file": [
            "starSED/phoSimMLT/lte034-4.5-1.0a+0.4.BT-Settl.spec.gz",
            "starSED/phoSimMLT/lte034-4.5-1.0a+0.4.BT-Settl.spec.gz",
            "starSED/phoSimMLT/lte034-4.5-1.0a+0.4.BT-Settl.spec.gz",
            "starSED/phoSimMLT/lte034-4.5-1.0a+0.4.BT-Settl.spec.gz",
        ],
        "length": [600., 600., 500., 2000.],
        "width": [1e-6, 1e-6, 1e-6, 1e-6],
        "position_angle": [0, 45, 60, 90],
    }
)
df0.to_parquet("satellite_streaks.parquet")
