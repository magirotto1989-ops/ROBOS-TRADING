import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from "react-native";
import { useState, useEffect, useCallback } from "react";
import { format, startOfDay, endOfDay, addDays } from "date-fns";
import { ptBR } from "date-fns/locale";
import { api, type Appointment } from "@/lib/api";

const STATUS_MAP: Record<string, { label: string; color: string; bg: string }> = {
  SCHEDULED: { label: "Agendada", color: "#B45309", bg: "#FEF3C7" },
  CONFIRMED: { label: "Confirmada", color: "#065F46", bg: "#D1FAE5" },
  CANCELLED: { label: "Cancelada", color: "#991B1B", bg: "#FEE2E2" },
  COMPLETED: { label: "Realizada", color: "#1E40AF", bg: "#DBEAFE" },
  NO_SHOW: { label: "Faltou", color: "#374151", bg: "#F3F4F6" },
};

export default function AgendaScreen() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedDate, setSelectedDate] = useState(new Date());

  const load = useCallback(async (date: Date) => {
    try {
      const data = await api.appointments.list({
        start: startOfDay(date).toISOString(),
        end: endOfDay(date).toISOString(),
      });
      setAppointments(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { load(selectedDate); }, [selectedDate, load]);

  const onRefresh = () => {
    setRefreshing(true);
    load(selectedDate);
  };

  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(new Date(), i - 3));

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#06B6D4" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Seletor de datas */}
      <View style={styles.dateStrip}>
        <FlatList
          horizontal
          data={weekDays}
          keyExtractor={(d) => d.toISOString()}
          showsHorizontalScrollIndicator={false}
          renderItem={({ item: day }) => {
            const isSelected = format(day, "yyyy-MM-dd") === format(selectedDate, "yyyy-MM-dd");
            const isToday = format(day, "yyyy-MM-dd") === format(new Date(), "yyyy-MM-dd");
            return (
              <TouchableOpacity
                style={[styles.dayBtn, isSelected && styles.dayBtnSelected]}
                onPress={() => setSelectedDate(day)}
              >
                <Text style={[styles.dayName, isSelected && styles.dayNameSelected]}>
                  {format(day, "EEE", { locale: ptBR }).toUpperCase()}
                </Text>
                <Text style={[styles.dayNum, isSelected && styles.dayNumSelected, isToday && !isSelected && styles.dayToday]}>
                  {format(day, "d")}
                </Text>
              </TouchableOpacity>
            );
          }}
        />
      </View>

      <Text style={styles.dateLabel}>
        {format(selectedDate, "EEEE, dd 'de' MMMM", { locale: ptBR })}
      </Text>

      {/* Lista de consultas */}
      <FlatList
        data={appointments}
        keyExtractor={(a) => a.id}
        contentContainerStyle={styles.list}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#06B6D4" />}
        ListEmptyComponent={() => (
          <View style={styles.empty}>
            <Text style={styles.emptyText}>Nenhuma consulta neste dia</Text>
          </View>
        )}
        renderItem={({ item }) => {
          const s = STATUS_MAP[item.status] ?? STATUS_MAP.SCHEDULED;
          return (
            <View style={styles.card}>
              <View style={styles.cardTime}>
                <Text style={styles.time}>{format(new Date(item.dateTime), "HH:mm")}</Text>
                <Text style={styles.duration}>{item.durationMin}min</Text>
              </View>
              <View style={styles.cardBody}>
                <Text style={styles.patientName}>{item.patient.name}</Text>
                <Text style={styles.profName}>{item.professional.name}</Text>
                <Text style={styles.specialty}>{item.professional.specialty}</Text>
                <View style={[styles.badge, { backgroundColor: s.bg }]}>
                  <Text style={[styles.badgeText, { color: s.color }]}>{s.label}</Text>
                </View>
              </View>
            </View>
          );
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F9FAFB" },
  center: { flex: 1, alignItems: "center", justifyContent: "center" },
  dateStrip: { backgroundColor: "#fff", paddingVertical: 12, paddingHorizontal: 8, borderBottomWidth: 1, borderBottomColor: "#F3F4F6" },
  dayBtn: { alignItems: "center", paddingHorizontal: 10, paddingVertical: 6, borderRadius: 12, marginHorizontal: 3 },
  dayBtnSelected: { backgroundColor: "#06B6D4" },
  dayName: { fontSize: 10, fontWeight: "600", color: "#6B7280" },
  dayNameSelected: { color: "#fff" },
  dayNum: { fontSize: 16, fontWeight: "700", color: "#111827", marginTop: 2 },
  dayNumSelected: { color: "#fff" },
  dayToday: { color: "#06B6D4" },
  dateLabel: { fontSize: 14, color: "#6B7280", paddingHorizontal: 16, paddingVertical: 10, textTransform: "capitalize" },
  list: { padding: 16, gap: 12 },
  card: { backgroundColor: "#fff", borderRadius: 12, padding: 14, flexDirection: "row", gap: 12, shadowColor: "#000", shadowOpacity: 0.04, shadowRadius: 8, elevation: 2 },
  cardTime: { alignItems: "center", justifyContent: "flex-start", paddingTop: 2, minWidth: 50 },
  time: { fontSize: 15, fontWeight: "700", color: "#06B6D4" },
  duration: { fontSize: 10, color: "#9CA3AF", marginTop: 2 },
  cardBody: { flex: 1 },
  patientName: { fontSize: 15, fontWeight: "600", color: "#111827" },
  profName: { fontSize: 13, color: "#4B5563", marginTop: 2 },
  specialty: { fontSize: 12, color: "#9CA3AF", marginTop: 1 },
  badge: { alignSelf: "flex-start", borderRadius: 20, paddingHorizontal: 8, paddingVertical: 3, marginTop: 6 },
  badgeText: { fontSize: 11, fontWeight: "600" },
  empty: { alignItems: "center", paddingTop: 60 },
  emptyText: { color: "#9CA3AF", fontSize: 15 },
});
