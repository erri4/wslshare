import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:fl_chart/fl_chart.dart';
//import 'package:intl/intl.dart';

void main() async {
  await Hive.initFlutter();
  await Hive.openBox('journal');
  runApp(const YomimonApp());
}

class YomimonApp extends StatelessWidget {
  const YomimonApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'יומימון',
      theme: ThemeData(primarySwatch: Colors.teal),
      home: const NavigationController(),
    );
  }
}

class NavigationController extends StatefulWidget {
  const NavigationController({super.key});

  @override
  State<NavigationController> createState() => _NavigationControllerState();
}

class _NavigationControllerState extends State<NavigationController> {
  int _index = 0;

  final pages = const [HomePage(), GraphsPage()];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: pages[_index],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _index,
        onTap: (i) => setState(() => _index = i),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'בית'),
          BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'גרפים'),
        ],
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int moodBefore = 3;
  int moodAfter = 3;
  int hydration = 1;
  int energy = 3;
  int participation = 3;
  int sleep = 1;
  final controllerBest = TextEditingController();
  final controllerHardest = TextEditingController();
  final controllerMemory = TextEditingController();
  final controllerLearned = TextEditingController();

  void saveEntry() async {
    final box = Hive.box('journal');
    final date = DateTime.now().toIso8601String().split('T')[0];
    final entry = {
      'moodBefore': moodBefore,
      'moodAfter': moodAfter,
      'hydration': hydration,
      'energy': energy,
      'participation': participation,
      'sleep': sleep,
      'best': controllerBest.text,
      'hardest': controllerHardest.text,
      'memory': controllerMemory.text,
      'learned': controllerLearned.text,
    };
    box.put(date, entry);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('היומן נשמר!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('יומימון')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('איך אני מרגיש/ה לפני היום?', style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              value: moodBefore.toDouble(),
              onChanged: (v) => setState(() => moodBefore = v.toInt()),
              min: 1,
              max: 5,
              divisions: 4,
              label: moodBefore.toString(),
            ),
            const Text('איך אני מרגיש/ה אחרי היום?', style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              value: moodAfter.toDouble(),
              onChanged: (v) => setState(() => moodAfter = v.toInt()),
              min: 1,
              max: 5,
              divisions: 4,
              label: moodAfter.toString(),
            ),
            const Text('כמה שתיתי?', style: TextStyle(fontWeight: FontWeight.bold)),
Row(
  children: List.generate(6, (index) => IconButton(
    icon: Icon(index == 0
        ? Icons.clear
        : (index <= hydration ? Icons.opacity : Icons.opacity_outlined)),
    onPressed: () => setState(() => hydration = index),
  )),
),
            const Text('רמת האנרגיה?', style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              value: energy.toDouble(),
              onChanged: (v) => setState(() => energy = v.toInt()),
              min: 1,
              max: 5,
              divisions: 4,
              label: energy.toString(),
            ),
            const Text('רמת ההשתתפות?', style: TextStyle(fontWeight: FontWeight.bold)),
            Slider(
              value: participation.toDouble(),
              onChanged: (v) => setState(() => participation = v.toInt()),
              min: 1,
              max: 5,
              divisions: 4,
              label: participation.toString(),
            ),
            const Text('כמה ישנתי?', style: TextStyle(fontWeight: FontWeight.bold)),
            DropdownButton<int>(
              value: sleep,
              onChanged: (v) => setState(() => sleep = v!),
              items: const [
                DropdownMenuItem(value: 0, child: Text('0-3')),
                DropdownMenuItem(value: 1, child: Text('4-6')),
                DropdownMenuItem(value: 2, child: Text('7-9')),
                DropdownMenuItem(value: 3, child: Text('10-12')),
              ],
            ),
            const SizedBox(height: 10),
            TextField(controller: controllerBest, decoration: const InputDecoration(labelText: 'מה היה לי הכי כיף?')),
            TextField(controller: controllerHardest, decoration: const InputDecoration(labelText: 'מה היה לי הכי מאתגר?')),
            TextField(controller: controllerMemory, decoration: const InputDecoration(labelText: 'משהו חשוב שאני רוצה לזכור')),
            TextField(controller: controllerLearned, decoration: const InputDecoration(labelText: 'מה למדתי ומה ארצה לשפר?')),
            const SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: saveEntry,
                child: const Text('שמור יומן'),
              ),
            )
          ],
        ),
      ),
    );
  }
}

class GraphsPage extends StatefulWidget {
  const GraphsPage({super.key});

  @override
  State<GraphsPage> createState() => _GraphsPageState();
}

class _GraphsPageState extends State<GraphsPage> {
  String viewType = 'weekly';

  List<MapEntry<dynamic, dynamic>> _getFilteredEntries(Box box) {
    final now = DateTime.now();
    final entries = box.toMap().entries.map((e) => MapEntry(e.key, e.value)).toList();
    entries.sort((a, b) => a.key.compareTo(b.key));
    return entries.where((e) {
      final date = DateTime.tryParse(e.key);
      if (date == null) return false;
      switch (viewType) {
        case 'daily':
          return date.day == now.day && date.month == now.month && date.year == now.year;
        case 'weekly':
          return now.difference(date).inDays <= 7;
        case 'monthly':
          return now.month == date.month && now.year == date.year;
        default:
          return true;
      }
    }).toList();
  }

  List<FlSpot> _generateData(List<MapEntry<dynamic, dynamic>> entries, String field) {
    return List.generate(entries.length, (i) {
      final value = entries[i].value[field] ?? 0;
      return FlSpot(i.toDouble(), (value as num).toDouble());
    });
  }

  Widget buildChart(Box box, String field, String label, Color color) {
  final filteredEntries = _getFilteredEntries(box);
  if (filteredEntries.isEmpty) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 40),
        const Text('אין נתונים להצגה', style: TextStyle(color: Colors.grey)),
        const SizedBox(height: 16),
      ],
    );
  }
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
      SizedBox(
        height: 150,
        child: LineChart(
          LineChartData(
            lineBarsData: [
              LineChartBarData(
                spots: _generateData(filteredEntries, field),
                isCurved: true,
                barWidth: 3,
                color: color,
                dotData: FlDotData(show: true),
              ),
            ],
            titlesData: FlTitlesData(
              show: true,
              leftTitles: AxisTitles(
                sideTitles: SideTitles(showTitles: true),
              ),
              bottomTitles: AxisTitles(
                sideTitles: SideTitles(showTitles: true),
              ),
            ),
            borderData: FlBorderData(show: true),
            gridData: FlGridData(show: true),
          ),
        ),
      ),
      const SizedBox(height: 16)
    ],
  );
}

  @override
  Widget build(BuildContext context) {
    final box = Hive.box('journal');
    return Scaffold(
      appBar: AppBar(
        title: const Text('גרפים'),
        actions: [
          DropdownButton<String>(
            value: viewType,
            onChanged: (v) => setState(() => viewType = v!),
            items: const [
              DropdownMenuItem(value: 'daily', child: Text('יומי')),
              DropdownMenuItem(value: 'weekly', child: Text('שבועי')),
              DropdownMenuItem(value: 'monthly', child: Text('חודשי')),
            ],
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            buildChart(box, 'moodBefore', 'מצב רוח לפני', Colors.blue),
            buildChart(box, 'moodAfter', 'מצב רוח אחרי', Colors.green),
            buildChart(box, 'hydration', 'שתייה', Colors.teal),
            buildChart(box, 'energy', 'אנרגיה', Colors.orange),
            buildChart(box, 'participation', 'השתתפות', Colors.purple),
            buildChart(box, 'sleep', 'שינה', Colors.brown),
          ],
        ),
      ),
    );
  }
}
