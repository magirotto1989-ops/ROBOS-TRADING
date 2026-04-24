import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import { useState, useEffect } from "react";
import { Ionicons } from "@expo/vector-icons";

type Patient = {
  id: string;
  name: string;
  phone: string;
  email?: string;
  cpf?: string;
  _count: { appointments: number };
};

export default function PacientesScreen() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const load = async (q = "") => {
    setLoading(true);
    try {
      const res = await fetch(`/api/patients?q=${encodeURIComponent(q)}&limit=30`);
      const data = await res.json();
      setPatients(data.patients ?? []);
    } catch {
      setPatients([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const formatPhone = (p: string) => {
    const d = p.replace(/\D/g, "");
    if (d.length >= 11) return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7, 11)}`;
    return p;
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchBar}>
        <Ionicons name="search" size={18} color="#9CA3AF" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar paciente..."
          placeholderTextColor="#9CA3AF"
          value={search}
          onChangeText={setSearch}
          onSubmitEditing={() => load(search)}
          returnKeyType="search"
        />
        {search.length > 0 && (
          <TouchableOpacity onPress={() => { setSearch(""); load(); }}>
            <Ionicons name="close-circle" size={18} color="#9CA3AF" />
          </TouchableOpacity>
        )}
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color="#06B6D4" />
        </View>
      ) : (
        <FlatList
          data={patients}
          keyExtractor={(p) => p.id}
          contentContainerStyle={styles.list}
          ListEmptyComponent={() => (
            <View style={styles.center}>
              <Text style={styles.emptyText}>Nenhum paciente encontrado</Text>
            </View>
          )}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>{item.name[0].toUpperCase()}</Text>
              </View>
              <View style={styles.info}>
                <Text style={styles.name}>{item.name}</Text>
                <Text style={styles.phone}>{formatPhone(item.phone)}</Text>
                {item.cpf && <Text style={styles.cpf}>CPF: {item.cpf}</Text>}
              </View>
              <View style={styles.count}>
                <Ionicons name="calendar-outline" size={14} color="#9CA3AF" />
                <Text style={styles.countText}>{item._count.appointments}</Text>
              </View>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F9FAFB" },
  center: { flex: 1, alignItems: "center", justifyContent: "center", paddingTop: 40 },
  searchBar: { flexDirection: "row", alignItems: "center", backgroundColor: "#fff", margin: 16, borderRadius: 12, paddingHorizontal: 12, paddingVertical: 10, shadowColor: "#000", shadowOpacity: 0.04, shadowRadius: 6, elevation: 2 },
  searchIcon: { marginRight: 8 },
  searchInput: { flex: 1, fontSize: 15, color: "#111827" },
  list: { padding: 16, gap: 10 },
  card: { backgroundColor: "#fff", borderRadius: 12, padding: 14, flexDirection: "row", alignItems: "center", gap: 12, shadowColor: "#000", shadowOpacity: 0.04, shadowRadius: 6, elevation: 1 },
  avatar: { width: 40, height: 40, borderRadius: 20, backgroundColor: "#CFFAFE", alignItems: "center", justifyContent: "center" },
  avatarText: { fontSize: 16, fontWeight: "700", color: "#0891B2" },
  info: { flex: 1 },
  name: { fontSize: 15, fontWeight: "600", color: "#111827" },
  phone: { fontSize: 13, color: "#6B7280", marginTop: 2 },
  cpf: { fontSize: 12, color: "#9CA3AF", marginTop: 1 },
  count: { alignItems: "center", gap: 2 },
  countText: { fontSize: 12, color: "#9CA3AF" },
  emptyText: { color: "#9CA3AF", fontSize: 15 },
});
