import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function PerfilScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>U</Text>
      </View>
      <Text style={styles.name}>Usuário</Text>
      <Text style={styles.email}>usuario@clinica.com</Text>

      <View style={styles.section}>
        <TouchableOpacity style={styles.item}>
          <Ionicons name="settings-outline" size={20} color="#6B7280" />
          <Text style={styles.itemText}>Configurações</Text>
          <Ionicons name="chevron-forward" size={16} color="#D1D5DB" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.item}>
          <Ionicons name="notifications-outline" size={20} color="#6B7280" />
          <Text style={styles.itemText}>Notificações</Text>
          <Ionicons name="chevron-forward" size={16} color="#D1D5DB" />
        </TouchableOpacity>
        <TouchableOpacity style={[styles.item, styles.logout]}>
          <Ionicons name="log-out-outline" size={20} color="#EF4444" />
          <Text style={[styles.itemText, styles.logoutText]}>Sair</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F9FAFB", alignItems: "center", paddingTop: 48 },
  avatar: { width: 80, height: 80, borderRadius: 40, backgroundColor: "#CFFAFE", alignItems: "center", justifyContent: "center" },
  avatarText: { fontSize: 32, fontWeight: "700", color: "#0891B2" },
  name: { fontSize: 20, fontWeight: "700", color: "#111827", marginTop: 12 },
  email: { fontSize: 14, color: "#6B7280", marginTop: 4 },
  section: { width: "100%", marginTop: 32, backgroundColor: "#fff", borderTopWidth: 1, borderBottomWidth: 1, borderColor: "#F3F4F6" },
  item: { flexDirection: "row", alignItems: "center", gap: 12, paddingHorizontal: 20, paddingVertical: 16, borderBottomWidth: 1, borderBottomColor: "#F9FAFB" },
  itemText: { flex: 1, fontSize: 15, color: "#374151" },
  logout: { borderBottomWidth: 0 },
  logoutText: { color: "#EF4444" },
});
