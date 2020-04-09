import matplotlib.pyplot as plt
import matplotlib.style
from conf import *
import numpy as np
import pickle

matplotlib.style.use('ggplot')


class Plot:
    def __init__(self, agents, plot_dir):
        self.agents = agents
        self.plot_dir = plot_dir
        plt.ion()
        self.fig, self.ax = plt.subplots(1, figsize=(7, 7))
        self.times = [0]
        self.values = np.array([self.get_infection_counts()])

    def update(self, t):
        self.times.append(t)

        infection_counts = self.get_infection_counts()

        self.values = np.append(self.values, [infection_counts], axis=0)

        if t % plot_interval == 1:
            self.ax.clear()

            self.ax.grid(True)
            self.ax.set_xlim(0, max(self.times))
            self.ax.set_ylim(0, max(self.values[:, 1]))

            self.ax.fill_between(self.times, 0, self.values[:, 1] +self.values[:, 0] +self.values[:, 2] +self.values[:, 3],
                                 color=np.array(agent_colors[3]) / 255)
            self.ax.fill_between(self.times, 0, self.values[:, 1] +self.values[:, 0] +self.values[:, 2],
                                 color=np.array(agent_colors[2]) / 255)
            self.ax.fill_between(self.times, 0, self.values[:, 1] +self.values[:, 0], color=np.array(agent_colors[0]) / 255)
            self.ax.fill_between(self.times, 0, self.values[:, 1], color=np.array(agent_colors[1]) / 255)

            health_care_values = np.minimum(health_system_capacity, self.values[:, 1])
            self.ax.fill_between(self.times, 0, health_care_values, color=np.array(agent_colors[1]) / 255 * 0.8 + 0.2)

            if fit_exponential:
                fit = np.polyfit(self.times, np.log(self.values[:, 1]), 1, w=np.sqrt(self.values[:, 1]))
                exp = np.exp(fit[1]) + np.exp(fit[0]*np.array(self.times))
                self.ax.plot(self.times, exp, color=(0.2, 0.2, 0.2))

            self.fig.tight_layout()
            self.fig.canvas.draw()
            self.fig.show()

            if do_record:
                self.fig.savefig("{}/plot_{:05d}.png".format(self.plot_dir, t))


    def get_infection_counts(self):
        infection_counts = [0, 0, 0, 0]
        for agent in self.agents:
            infection_counts[agent.infection] += 1
        return infection_counts

    def close(self):
        pickle.dump((self.times, self.values), open(".tmp.p", "wb"))
        plt.close('all')