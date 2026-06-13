import streamlit as st
import random
import time
from collections import deque

# Configuración
st.set_page_config(page_title="Bratz Fashion Store", page_icon="💄", layout="wide")

# Estilos
st.markdown("""
<style>
    .titulo { text-align:center; font-size:50px; font-weight:bold; color:#ff1493; }
    .card { background:white; padding:20px; border-radius:20px; box-shadow:0px 4px 10px rgba(0,0,0,.1); margin:10px; }
    .producto { background:#fff0f7; border-left:5px solid hotpink; padding:8px; border-radius:5px; margin:5px 0; }
</style>
""", unsafe_allow_html=True)

# Lógica
class CajaBratz:
    def __init__(self, saldo=5000): self.saldo = saldo
    def agregar_venta(self, monto): self.saldo += monto

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
    def agregar_producto(self, nombre, precio): self.productos.append((nombre, precio))
    @property
    def total(self): return sum(precio for _, precio in self.productos)

clientes = ["Cloe", "Yasmin", "Jade", "Sasha", "Cameron", "Dylan"]
munecas = [("Bratz Core", 650), ("Winter Glam", 750), ("Rock Angelz", 890), ("Designer Edition", 1200)]
accesorios = [("Maquillaje", 150), ("Bolso", 220), ("Zapatos Plataforma", 180), ("Gafas de Sol", 90)]

# Interfaz
st.markdown('<div class="titulo">💄 BRATZ 💄</div>', unsafe_allow_html=True)

if st.button("🚀 Iniciar Simulación"):
    cola = deque(clientes)
    pila = []
    caja = CajaBratz()
    
    # Crear contenedores estables
    col1, col2, col3 = st.columns(3)
    c1 = col1.container()
    c2 = col2.container()
    c3 = col3.container()
    stats = st.empty()

    while cola:
        cliente = cola.popleft()
        pedido = Pedido(cliente)
        
        # Productos
        m, p = random.choice(munecas)
        pedido.agregar_producto(m, p)
        for _ in range(random.randint(0, 2)):
            a, p_a = random.choice(accesorios)
            pedido.agregar_producto(a, p_a)
            
        caja.agregar_venta(pedido.total)
        pila.append({"c": cliente, "t": pedido.total})

        # Actualizar contenedores (esto evita el error de nodos)
        c1.markdown(f'<div class="card"><h3>👥 Cola</h3><h1>{len(cola)}</h1> clientes esperando</div>', unsafe_allow_html=True)
        prods_html = "".join([f'<div class="producto">{n} - ${pr}</div>' for n, pr in pedido.productos])
        c2.markdown(f'<div class="card"><h3>🛍️ Cliente Actual</h3><b>{cliente}</b>{prods_html}<b>Total: ${pedido.total}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card"><h3>📄 Ticket</h3>Cliente: {cliente}<br>Total: ${pedido.total}</div>', unsafe_allow_html=True)
        stats.metric("💰 Dinero en Caja", f"${caja.saldo:.2f}")
        
        time.sleep(1.5)
    
    st.success("✅ Simulación completada")