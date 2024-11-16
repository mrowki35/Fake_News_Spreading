import agentpy as ap
import networkx as nx
import matplotlib.pyplot as plt


class UserAgent(ap.Agent):
    """Klasa reprezentująca użytkownika w modelu."""

    def setup(self):
        # Inicjalizacja stanu agenta
        self.state = 'S'  # Domyślnie wszyscy agenci są w stanie podatnym (Susceptible)

    def update_state(self):
        """Aktualizacja stanu agenta na podstawie reguł przejść."""
        if self.state == 'S':
            # Sprawdzenie, czy sąsiedzi w stanie 'I' narażają agenta na dezinformację
            infected_neighbors = [n for n in self.model.network.neighbors(self.id)
                                  if self.model.agents[n].state == 'I']
            if infected_neighbors:
                if self.model.p['beta'] > self.model.random.random():
                    self.state = 'E'

        elif self.state == 'E':
            # Decyzja, czy agent przejdzie do stanu 'I' czy 'D'
            rand = self.model.random.random()
            if rand < self.model.p['alpha']:
                self.state = 'I'
            elif rand < self.model.p['alpha'] + self.model.p['gamma']:
                self.state = 'D'

        elif self.state == 'I':
            # Możliwość przejścia do stanu 'R'
            if self.model.p['delta'] > self.model.random.random():
                self.state = 'R'

        elif self.state == 'D':
            # Możliwość ponownej ekspozycji na dezinformację
            infected_neighbors = [n for n in self.model.network.neighbors(self.id)
                                  if self.model.agents[n].state == 'I']
            if infected_neighbors:
                if self.model.p['theta'] > self.model.random.random():
                    self.state = 'E'


class DisinformationModel(ap.Model):
    """Klasa modelu symulującego rozprzestrzenianie się dezinformacji."""

    def setup(self):
        # Tworzenie grafu sieci społecznej
        self.network = nx.erdos_renyi_graph(n=self.p.N, p=self.p.connect_prob)

        # Dodawanie agentów do modelu
        self.agents = ap.AgentList(self, self.p.N, UserAgent)
        for i, agent in enumerate(self.agents):
            agent.id = i  # Przypisanie indeksu agenta zgodnie z węzłem w grafie

        # Przypisywanie agentów do węzłów grafu
        mapping = dict(zip(self.network.nodes, range(self.p.N)))
        self.network = nx.relabel_nodes(self.network, mapping)

        # Inicjalizacja początkowych stanów agentów
        initial_infected = self.random.sample(self.agents, k=self.p.initial_infected)
        for agent in initial_infected:
            agent.state = 'I'

        # Konfiguracja zbierania danych
        self.datacollector = ap.DataCollector(
            {
                'S': lambda m: sum(1 for a in m.agents if a.state == 'S'),
                'E': lambda m: sum(1 for a in m.agents if a.state == 'E'),
                'I': lambda m: sum(1 for a in m.agents if a.state == 'I'),
                'D': lambda m: sum(1 for a in m.agents if a.state == 'D'),
                'R': lambda m: sum(1 for a in m.agents if a.state == 'R'),
            }
        )

        self.datacollector.collect(self)

    def step(self):
        # Aktualizacja stanu każdego agenta
        for agent in self.agents:
            agent.update_state()

        # Zbieranie danych po każdym kroku
        self.datacollector.collect(self)

    def end(self):
        # Zakończenie symulacji
        pass


# Parametry modelu
parameters = {
    'N': 1000,  # Liczba agentów
    'connect_prob': 0.01,  # Prawdopodobieństwo połączenia w grafie losowym
    'initial_infected': 10,  # Początkowa liczba agentów w stanie 'I'
    'steps': 50,  # Liczba kroków symulacji
    'beta': 0.3,  # Współczynnik rozprzestrzeniania dezinformacji
    'alpha': 0.5,  # Prawdopodobieństwo przejścia z 'E' do 'I'
    'gamma': 0.3,  # Współczynnik sceptycyzmu (przejście z 'E' do 'D')
    'delta': 0.2,  # Prawdopodobieństwo przejścia z 'I' do 'R'
    'theta': 0.1  # Współczynnik ponownej ekspozycji z 'D' do 'E'
}

# Inicjalizacja i uruchomienie modelu
model = DisinformationModel(parameters)
results = model.run()

# Wykres wyników
data = results.variables

plt.figure(figsize=(10, 6))
plt.plot(data['t'], data['S'], label='S (Podatni)')
plt.plot(data['t'], data['E'], label='E (Narażeni)')
plt.plot(data['t'], data['I'], label='I (Zainfekowani)')
plt.plot(data['t'], data['D'], label='D (Sceptyczni)')
plt.plot(data['t'], data['R'], label='R (Odporni)')
plt.xlabel('Krok symulacji')
plt.ylabel('Liczba agentów')
plt.title('Symulacja rozprzestrzeniania się dezinformacji')
plt.legend()
plt.show()
