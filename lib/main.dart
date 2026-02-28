
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(MaterialApp(
    theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue), useMaterial3: true),
    home: EBayCameraApp(cameras: cameras),
    debugShowCheckedModeBanner: false,
  ));
}

class EBayCameraApp extends StatefulWidget {
  final List<CameraDescription> cameras;
  const EBayCameraApp({super.key, required this.cameras});
  @override
  State<EBayCameraApp> createState() => _EBayCameraAppState();
}

class _EBayCameraAppState extends State<EBayCameraApp> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  String _category = 'Tops';
  int _counter = 100;
  final TextEditingController _notesController = TextEditingController();
  final Map<String, XFile?> _photos = {
    'Front': null, 'Back': null, 'Length_Inseam': null, 
    'Width_Waist': null, 'Tags': null, 'Imperfections': null,
  };

  @override
  void initState() {
    super.initState();
    _loadCounter();
    _controller = CameraController(widget.cameras.first, ResolutionPreset.high);
    _initializeControllerFuture = _controller.initialize();
  }

  _loadCounter() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() => _counter = prefs.getInt('item_counter') ?? 100);
  }

  Future<void> _saveItem() async {
    final directory = await getApplicationDocumentsDirectory();
    final String folderName = "${_category}_$_counter";
    final String zackPath = p.join(directory.path, 'Zack', folderName);
    final itemDir = Directory(zackPath);
    if (!await itemDir.exists()) await itemDir.create(recursive: true);

    for (var entry in _photos.entries) {
      if (entry.value != null) {
        final String newPath = p.join(zackPath, "${entry.key.toLowerCase()}.jpg");
        await File(entry.value!.path).copy(newPath);
      }
    }
    await File(p.join(zackPath, 'notes.txt')).writeAsString(_notesController.text);

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Saved to Zack/$folderName')));
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _counter++;
      prefs.setInt('item_counter', _counter);
      _photos.updateAll((key, value) => null);
      _notesController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Inventory #$_counter'), actions: [
        DropdownButton<String>(
          value: _category,
          items: ['Tops', 'Bottoms'].map((v) => DropdownMenuItem(value: v, child: Text(v))).toList(),
          onChanged: (v) => setState(() => _category = v!),
        )
      ]),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        AspectRatio(aspectRatio: 1, child: FutureBuilder(
          future: _initializeControllerFuture,
          builder: (context, snap) => snap.connectionState == ConnectionState.done ? CameraPreview(_controller) : const Center(child: CircularProgressIndicator()),
        )),
        ..._photos.keys.map((type) => ListTile(
          title: Text(type),
          trailing: _photos[type] != null ? const Icon(Icons.check, color: Colors.green) : IconButton(icon: const Icon(Icons.camera_alt), onPressed: () async {
            final img = await _controller.takePicture();
            setState(() => _photos[type] = img);
          }),
        )),
        TextField(controller: _notesController, decoration: const InputDecoration(labelText: 'Notes')),
        const SizedBox(height: 20),
        ElevatedButton(onPressed: _photos['Front'] == null ? null : _saveItem, child: const Text('SAVE ITEM')),
      ])),
    );
  }
}
