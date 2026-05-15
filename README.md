# GBase Resource Plans Timelines Simulation

This example simulates how a database system like GBase 8a might integrate resource plans with timelines. It demonstrates how different workload types (e.g., OLTP queries, reporting queries, batch jobs) receive varying resource priorities based on the time of day or week, optimizing performance for critical operations during peak hours and allowing batch jobs to run efficiently during off-peak times.

## Language

`python`

## How to Run

Save the code as `main.py`. Run from your terminal using `python main.py`. Observe how workload processing priorities change based on the simulated time and active resource plan.

## Original Article

This example accompanies the Turkish article: [GBase 8a Kaynak Planları Zaman Çizelgeleriyle Nasıl Entegre Edilir?](https://fatihsoysal.com/blog/gbase-8a-kaynak-planlari-zaman-cizelgeleriyle-nasil-entegre-edilir/).

## License

MIT — see [LICENSE](LICENSE).
